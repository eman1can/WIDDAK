from os.path import join

from gdpc.template import Template
from src.vox import VoxFile

vox_file = VoxFile.from_file(r'MarkovJunior/resources/rules/ModernHouseMOD2/ModernHouseMOD1_73618823.vox')
template = Template.from_vox_model('Modern House', vox_file.get_model(), vox_file.get_color_palette())
template.to_file(join('local', 'templates', 'modern_house'))
