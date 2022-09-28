import random
from typing import List, Dict

import numba
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from terrain import TerrainMaps
from terrain.map import Map
from utils import Point, product, full, BuildArea, bernouilli, euclidean, X_ARRAY, Z_ARRAY
from utils.misc_objects_functions import argmax, argmin, _in_limits


class Districts(Map):
    """
    Districts construction -> partitions the build area and select zones that will become settlements.
    Was implemented to add structure to large inputs

    As instance of Map, holds local "density", ie a scalar value indicating how close we are to a city center.
    0 = city center
    ~1 = downtown
    ~2/3 = outskirts
    more = countryside
    """
    def __init__(self, area: BuildArea):
        super().__init__(np.ones((area.width, area.length)))
        self.__cluster_map = full((self.width, self.length), 0)
        self.__scaler = StandardScaler()
        self.__coord_scale = 1
        self.district_centers: List[Point] = None  # All district centers (ie means of kmeans)
        self.town_centers: List[Point] = None  # Subset of district centers, which are meant to be built on
        self.district_map: Map = None
        self.cluster_size = {}
        self.cluster_suitability = {}
        self.town_indexes = set()  # indexes of built districts
        self.seeders: Dict[int, DistrictSeeder] = {}
        self.name_gen = CityNameGenerator()
        self.town_names = {}

    def build(self, maps: TerrainMaps, **kwargs):
        visualize = kwargs.get("visualize", False)
        X, Xu = self.__build_data(maps)
        cluster_approx = np.sqrt(self.width * self.length) // 50
        print("cluster approx", cluster_approx)
        min_clusters = int(cluster_approx / 2)
        max_clusters = int(np.ceil(cluster_approx * 1.3))
        if max_clusters < 2:
            kwargs["n_clusters"] = 1
        print(f"there'll be between {min_clusters} and {max_clusters} districts")
        min_clusters = max(2, min_clusters)

        if max_clusters - min_clusters < 8:
            possible_k = range(min_clusters, max_clusters + 1)
        else:
            gamma = (max_clusters / min_clusters) ** (1/8)
            possible_k = {int(round(min_clusters * (gamma**k))) for k in range(8)}

        def select_best_model():
            if kwargs.get("n_clusters", 0):
                return self.__kmeans(X, kwargs.get("n_clusters"), visualize)

            models, scores = [], []
            for n_clusters in possible_k:
                model: KMeans = self.__kmeans(X, n_clusters, visualize)
                models.append(model)
                if X.shape[0] < 10000:
                    scores.append(silhouette_score(X, model.labels_))
                else:
                    sample = np.random.randint(X.shape[0], size=10000)
                    scores.append(silhouette_score(X[sample, :], model.labels_[sample]))
                print("silhouette", scores[-1])

            if visualize:
                plt.plot(range(2, max_clusters + 1), scores)
                plt.title("Silhouette score as a function of n_clusters")
                plt.show()

            index = argmax(range(len(models)), key=lambda i: scores[i])
            return models[index]

        model = select_best_model()

        labels = set(model.labels_)
        for label in labels:
            cluster = Xu[model.labels_ == label]
            score = cluster[:, 2].mean()
            self.cluster_suitability[label] = score
            self.cluster_size[label] = cluster.shape[0]

        centers = self.__scaler.inverse_transform(model.cluster_centers_ / self.__coord_scale)
        seeds = [Point(round(_[0]), round(_[1])) for _ in centers]
        samples = [Point(Xu[i, 0], Xu[i, 1]) for i in range(Xu.shape[0])]
        self.district_centers = [argmin(samples, key=lambda sample: euclidean(seed, sample)) for seed in seeds]

        map_center = Point(maps.width // 2, maps.length // 2)
        if min(euclidean(map_center, district) for district in self.district_centers) > 15:
            # todo: under the assumption that the GDMC judges will spawn at the middle of the building area,
            #  we place a marker there so that they can find their way
            self.district_centers.append(map_center)

        def select_town_clusters():
            surface_to_build = X.shape[0] * .7
            surface_built = 0
            best_suitability = max(self.cluster_suitability.values())
            for index, _ in sorted(self.cluster_suitability.items(), key=lambda _: _[1], reverse=True):
                self.town_indexes.add(index)
                self.town_names[self.district_centers[index]] = self.name_gen.generate()
                self.seeders[index] = DistrictSeeder(
                    self.district_centers[index],
                    Xu[:, 0][model.labels_ == label].std(),
                    Xu[:, 1][model.labels_ == label].std()
                )
                surface_built += self.cluster_size[index]
                if surface_built >= surface_to_build or self.cluster_suitability[index] < best_suitability / 2:
                    break
            return list(sorted(self.town_indexes, key=(lambda i: self.cluster_suitability[i]), reverse=True))

        town_indexes = select_town_clusters()
        self.town_centers = [self.district_centers[index] for index in town_indexes]

        self.__build_cluster_map(model, Xu, town_indexes)

    def __build_data(self, maps: TerrainMaps, coord_scale=1.15):
        n_samples = min(1e5, self.width * self.length)
        keep_rate = n_samples / (self.width * self.length)
        Xu = np.array([[x, z, Districts.suitability(x, z, maps)]
                      for x, z in product(range(maps.width), range(maps.length))
                      if bernouilli(keep_rate) and not maps.fluid_map.is_close_to_fluid(x, z)])
        X = self.__scaler.fit_transform(Xu)
        X[:, :2] = X[:, :2] * coord_scale
        self.__coord_scale = coord_scale
        print(f"{X.shape[0]} samples to select districts")
        return X, Xu

    def __kmeans(self, X: np.ndarray, n_clusters, visualize=False, coord_scale=1.15):
        print(f"Selecting {n_clusters} districts")
        kmeans = KMeans(n_clusters=n_clusters, tol=1e-5).fit(X)
        if visualize:
            Xu = self.__scaler.inverse_transform(X)
            x, y = Xu[:, 0], -Xu[:, 1]
            color = ["#" + ''.join([random.choice("ABCDEF0123456789") for j in range(6)]) for i in range(len(kmeans.cluster_centers_))]
            c = [color[cluster] for cluster in kmeans.labels_]
            plt.scatter(x, y, c=c)
            xc = self.__scaler.inverse_transform(kmeans.cluster_centers_)[:, 0]
            yc = -self.__scaler.inverse_transform(kmeans.cluster_centers_)[:, 1]
            plt.scatter(xc, yc, s=100, c='k', marker='+')
            plt.title(f"{n_clusters} clusters - scaling factor: {coord_scale}")
            plt.show()

        return kmeans

    @staticmethod
    def suitability(x, z, terrain: TerrainMaps):
        return np.exp(-terrain.height_map.steepness(x, z))  # higher steepness = lower suitability

    def __build_cluster_map(self, clusters: KMeans, samples: np.ndarray, town_indexes: List[int]):
        town_score = {label: 1 / (index + 1) for (index, label) in enumerate(town_indexes)}
        label_score = np.array([town_score[label] if (label in town_score) else 0 for label in range(max(clusters.labels_) + 1)], dtype=np.float32)
        propagation = KNeighborsClassifier(n_neighbors=3, n_jobs=-1)
        propagation.fit(samples[:, :2], clusters.labels_)

        # all locations of the build area in a flattened array
        distribution = np.array([[x, z] for x, z in product(range(self.width), range(self.length))])

        # cluster index for each of these locations
        neighborhood = propagation.predict(distribution)  # type: np.ndarray

        # reshaped cluster matrix
        neighborhood = neighborhood.reshape((self.width, self.length))

        # transform this matrix to interest of building here
        values = np.vectorize(lambda label: label_score[label])(neighborhood)

        # store results
        self.district_map = Map(neighborhood)
        self.score_map = Map(values)

        density_matrix = None
        for town_index in self.town_indexes:
            center = self.district_centers[town_index]
            dist = self.seeders[town_index]
            sig_x = dist.stdev_x
            sig_z = dist.stdev_z

            if density_matrix is None:
                density_matrix = density_one_district((center.x, center.z), (sig_x, sig_z))
            else:
                district_density = density_one_district((center.x, center.z), (sig_x, sig_z))
                density_matrix = np.minimum(density_matrix, district_density)

        self._values = density_matrix

    @property
    def n_districts(self):
        return len(self.district_centers)

    @property
    def buildable_surface(self):
        return sum(self.cluster_size[i] for i in self.town_indexes)

    def seed(self):
        """
        Returns a random position suitable for building
        """
        town_centers = list(self.town_indexes)
        town_cluster_probs = [self.cluster_size[i] for i in town_centers]
        town_cluster_probs = np.array(town_cluster_probs) / sum(town_cluster_probs)
        while True:
            seed_cluster = np.random.choice(town_centers, p=town_cluster_probs)
            seed: Point = self.seeders[seed_cluster].seed()
            if _in_limits(seed.coords, self.width, self.length):
                return seed


class DistrictSeeder:
    """
    Seeds positions for new parcels in this district
    """
    def __init__(self, district_center, sigma_x, sigma_z):
        self.__center = district_center
        self.n_parcels = 0
        self.stdev_x = sigma_x
        self.stdev_z = sigma_z

    def seed(self):
        """
        :return: (Point) position for a new parcel
        """
        x = random.normalvariate(self.__center.x, self.stdev_x)
        z = random.normalvariate(self.__center.z, self.stdev_z)
        return Point(int(round(x)), int(round(z)))


class CityNameGenerator:
    """
    Simple name generator based on French cities
    Sample names are split around consonants and vowels and linked in a markov chain.
    This same Markov Chain is explored to generate new names
    """
    INPUT = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Montpellier",
             "Strasbourg", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-etienne",
             "Toulon", "Grenoble", "Dijon", "Angers", "Nimes", "Villeurbanne", "Saint-Denis",
             "Le Mans", "Aix-en-Provence", "Clermont-Ferrand", "Brest", "Tours", "Limoges",
             "Amiens", "Annecy", "Perpignan", "Boulogne-Billancourt", "Metz", "Besançon",
             "Orleans", "Saint-Denis", "Argenteuil", "Mulhouse", "Rouen", "Montreuil", "Caen",
             "Saint-Paul", "Nancy", "Noumea", "Tourcoing", "Roubaix", "Nanterre",
             "Vitry-sur-Seine", "Avignon", "Creteil", "Dunkerque", "Poitiers",
             "Asnieres-sur-Seine", "Versailles", "Colombes", "Saint-Pierre", "Aubervilliers",
             "Aulnay-sous-Bois", "Courbevoie", "Fort-de-France", "Cherbourg-en-Cotentin",
             "Rueil-Malmaison", "Pau", "Champigny-sur-Marne", "Le Tampon", "Beziers", "Calais",
             "La Rochelle", "Saint-Maur-des-Fosses", "Antibes", "Cannes", "Mamoudzou", "Colmar",
             "Merignac", "Saint-Nazaire", "Drancy", "Issy-les-Moulineaux", "Ajaccio",
             "Noisy-le-Grand", "Bourges", "La Seyne-sur-Mer", "Venissieux", "Levallois-Perret",
             "Quimper", "Cergy", "Valence", "Villeneuve-d'Ascq", "Antony", "Pessac", "Troyes",
             "Neuilly-sur-Seine", "Clichy", "Montauban", "Chambery", "Ivry-sur-Seine", "Niort",
             "Cayenne", "Lorient", "Sarcelles", "Villejuif", "Hyeres", "Saint-Andre",
             "Saint-Quentin", "Les Abymes", "Le Blanc-Mesnil", "Pantin", "Maisons-Alfort",
             "Beauvais", "epinay-sur-Seine", "evry", "Chelles", "Cholet", "Meaux",
             "Fontenay-sous-Bois", "La Roche-sur-Yon", "Saint-Louis", "Narbonne", "Bondy",
             "Vannes", "Frejus", "Arles", "Clamart", "Sartrouville", "Bobigny", "Grasse", "Sevran",
             "Corbeil-Essonnes", "Laval", "Belfort", "Albi", "Vincennes", "evreux", "Martigues",
             "Cagnes-sur-Mer", "Bayonne", "Montrouge", "Suresnes", "Saint-Ouen", "Massy",
             "Charleville-Mezieres", "Brive-la-Gaillarde", "Vaulx-en-Velin", "Carcassonne",
             "Saint-Herblain", "Saint-Malo", "Blois", "Aubagne", "Chalon-sur-Saone", "Meudon",
             "Chalons-en-Champagne", "Puteaux", "Saint-Brieuc", "Saint-Priest",
             "Salon-de-Provence", "Mantes-la-Jolie", "Rosny-sous-Bois", "Gennevilliers",
             "Livry-Gargan", "Alfortville", "Bastia", "Valenciennes", "Choisy-le-Roi",
             "Chateauroux", "Sete", "Saint-Laurent-du-Maroni", "Noisy-le-Sec", "Istres",
             "Garges-les-Gonesse", "Boulogne-sur-Mer", "Caluire-et-Cuire", "Talence",
             "Angoulême", "La Courneuve", "Le Cannet", "Castres", "Wattrelos", "Bourg-en-Bresse",
             "Gap", "Arras", "Bron", "Thionville", "Tarbes", "Draguignan", "Compiegne",
             "Le Lamentin", "Douai", "Saint-Germain-en-Laye", "Melun", "Reze", "Gagny", "Stains",
             "Ales", "Bagneux", "Marcq-en-Baroeul", "Chartres", "Colomiers", "Anglet",
             "Saint-Martin-d'Heres", "Montelimar", "Pontault-Combault", "Saint-Benoit",
             "Saint-Joseph", "Joue-les-Tours", "Chatillon", "Poissy", "Montluçon",
             "Villefranche-sur-Saone", "Villepinte", "Savigny-sur-Orge", "Bagnolet",
             "Sainte-Genevieve-des-Bois", "echirolles", "La Ciotat", "Creil", "Le Port",
             "Annemasse", "Saint-Martin ", "Conflans-Sainte-Honorine", "Thonon-les-Bains",
             "Saint-Chamond", "Roanne", "Neuilly-sur-Marne", "Auxerre", "Tremblay-en-France",
             "Saint-Raphaël", "Franconville", "Haguenau", "Nevers", "Vitrolles", "Agen",
             "Le Perreux-sur-Marne", "Marignane", "Saint-Leu", "Romans-sur-Isere",
             "Six-Fours-les-Plages", "Chatenay-Malabry", "Macon", "Montigny-le-Bretonneux",
             "Palaiseau", "Cambrai", "Sainte-Marie", "Meyzieu", "Athis-Mons", "La Possession",
             "Villeneuve-Saint-Georges", "Matoury", "Trappes", "Koungou", "Les Mureaux",
             "Houilles", "epinal", "Plaisir", "Dumbea", "Chatellerault", "Schiltigheim",
             "Villenave-d'Ornon", "Nogent-sur-Marne", "Lievin", "Baie-Mahault", "Chatou",
             "Goussainville", "Dreux", "Viry-Chatillon", "L'Haÿ-les-Roses", "Vigneux-sur-Seine",
             "Charenton-le-Pont", "Mont-de-Marsan", "Saint-Medard-en-Jalles", "Pontoise",
             "Cachan", "Lens", "Rillieux-la-Pape", "Savigny-le-Temple", "Maubeuge",
             "Clichy-sous-Bois", "Dieppe", "Vandoeuvre-les-Nancy", "Malakoff", "Perigueux",
             "Aix-les-Bains", "Vienne", "Sotteville-les-Rouen", "Saint-Laurent-du-Var",
             "Saint-etienne-du-Rouvray", "Soissons", "Saumur", "Vierzon", "Alençon", "Vallauris",
             "Aurillac", "Le Grand-Quevilly", "Montbeliard", "Saint-Dizier", "Vichy", "Biarritz",
             "Orly", "Bruay-la-Buissiere", "Le Creusot"]

    def __init__(self):
        self.beg_symbol = set()
        self.end_symbol = set()
        self.transition = {}
        self.__name_trash = set()
        
        for name in self.INPUT:
            self.register_name(name)

    vowels = 'aeiouy'
    punctuation = " -'"
    
    def parse_city_name(self, true_name: str):
        substrings = []
        current_sub = true_name.lower()[0]

        def is_vowel():
            return letter in self.vowels

        def doing_vowels():
            return current_sub[0] in self.vowels

        for letter in true_name.lower()[1:]:
            if letter in self.punctuation or current_sub[0] in self.punctuation or doing_vowels() ^ is_vowel():
                substrings.append(current_sub)
                current_sub = letter
            else:
                current_sub += letter
        substrings.append(current_sub)

        return substrings
    
    def register_name(self, city_name):
        substrings = self.parse_city_name(city_name)
        self.beg_symbol.add(substrings[0] + substrings[1])
        self.end_symbol.add(substrings[-2] + substrings[-1])
        for index in range(len(substrings) - 2):
            sym = substrings[index] + substrings[index + 1]
            bol = substrings[index + 2]
            if sym not in self.transition:
                self.transition[sym] = []
            self.transition[sym].append(bol)
        for index in range(len(substrings) - 1):
            sym = substrings[index]
            bol = substrings[index + 1]
            if sym not in self.transition:
                self.transition[sym] = []
            self.transition[sym].append(bol)
            
    def split_symbol(self, substring):
        if substring[0] in self.punctuation:
            return substring[0], substring[1:]
        elif substring[-1] in self.punctuation:
            return substring[:-1], substring[-1]

        def is_vowel():
            return substring[0] in self.vowels

        def doing_vowels():
            return substring[i] in self.vowels
        
        for i in range(len(substring)):
            if is_vowel() ^ doing_vowels():
                return substring[:i], substring[i:]
            
        return substring, substring

    def sample(self):
        """
        Sample one name
        :return: generated name
        """
        name = symbol = random.choice(list(self.beg_symbol))
        while not (symbol in self.end_symbol and (bernouilli(len(name) / 16)) or symbol not in self.transition):
            sym, bol = self.split_symbol(symbol)
            if bernouilli():
                symbol = bol
            new = random.choice(self.transition[symbol])
            name += new
            symbol = bol + new
        return name.capitalize()

    def generate(self):
        """
        Sample a bunch of names, return the one it prefers and stores it so that it doesn't appear again
        """
        while True:
            name = self.sample()
            if (6 < len(name) < 14)\
                    and ('-' not in name)\
                    and (name not in self.INPUT)\
                    and name not in self.__name_trash:
                self.__name_trash.add(name)
                return name


@numba.njit()
def density_one_district(xz, sigma):
    x, z = xz
    sig_x, sig_z = sigma

    x_dist = np.abs(X_ARRAY - x) / sig_x
    z_dist = np.abs(Z_ARRAY - z) / sig_z

    dist = np.sqrt(x_dist ** 2 + z_dist ** 2)
    return dist


if __name__ == '__main__':
    gen = CityNameGenerator()
    for _ in range(10):
        print(gen.generate())
