import urllib.request
from os import makedirs, remove
import zipfile
from os.path import join

data = """
<div class="alert alert-minecraft-stonebrick">
            <nav>
              <div class="nav nav-tabs" id="nav-tab" role="tablist">
                
                  <button class="nav-link nav-link-gold" id="nav-2022-tab" data-bs-toggle="tab" data-bs-target="#nav-2022" type="button" role="tab" aria-controls="nav-2022" aria-selected="false">
                    2022
                  </button>
                  
                    <button class="nav-link nav-link-gold" id="nav-2021-tab" data-bs-toggle="tab" data-bs-target="#nav-2021" type="button" role="tab" aria-controls="nav-2021" aria-selected="false">
                      2021
                    </button>
                    
                    <button class="nav-link nav-link-gold" id="nav-2020-tab" data-bs-toggle="tab" data-bs-target="#nav-2020" type="button" role="tab" aria-controls="nav-2020" aria-selected="false">
                      2020
                    </button>
                    
                    <button class="nav-link nav-link-gold" id="nav-2019-tab" data-bs-toggle="tab" data-bs-target="#nav-2019" type="button" role="tab" aria-controls="nav-2019" aria-selected="false">
                      2019
                    </button>
                    
                    <button class="nav-link nav-link-gold active" id="nav-2018-tab" data-bs-toggle="tab" data-bs-target="#nav-2018" type="button" role="tab" aria-controls="nav-2018" aria-selected="true">
                      2018
                    </button>
                    
              </div>
            </nav>

            <div class="tab-content" id="nav-tabContent">
              
                <div class="tab-pane fade" id="nav-2022" role="tabpanel" aria-labelledby="nav-2022-tab">
                  

  <div class="row">
  <div class="d-flex justify-content-center">
    <a href="/" ,="" target="_blank" style="color:gold;">Download the base maps HERE</a>
  </div>
</div>

<div class="row">
<div class="table-responsive">
  <table class="table table-dark table-striped table-bordered align-middle">
    <thead>
      <tr>
        <th scope="col">Entry</th>
        <th scope="col">Generator Name</th>
        <th scope="col">Team Name</th>
        <th scope="col">Affiliation</th>
        
        <th scope="col">
          Adaptability
        </th>
        
        <th scope="col">
          Functionality
        </th>
        
        <th scope="col">
          Narrative
        </th>
        
        <th scope="col">
          Aesthetic
        </th>
        
        <th scope="col">
          Overall
        </th>
        
        <th scope="col">Maps</th>
        <th scope="col">Code</th>
      </tr>
    </thead>
    <tbody>
      
      <tr>
        <td scope="row">0
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">PandaVision</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          PandaVision</td>
        <td>Intelligent</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">1
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">GDMC_CLIENT</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          GW</td>
        <td>Intelligent Entertainment Laboratory, Ritsumei</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">2
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">PCGNN</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Wits PCGNN</td>
        <td>University of the Witwatersrand, Johannesburg</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">3
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Cozy City Gen</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Alexis and Youri - Tsukuba tea</td>
        <td>Tsukuba Team</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">4
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Mc-CycleGAN </td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Team Sebastian Chr. v2</td>
        <td>University of Southern Denmark</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">5
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Immersive and Realist Minecraf...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          La team baguette</td>
        <td>-</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">6
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Avarice</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          PolyRifts</td>
        <td>-</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">7
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Leifsbu</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Terje Schjelderup</td>
        <td>-</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">8
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">DouceFranceV2</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          CharlieMDRz</td>
        <td>-</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">9
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Agent-based Medieval City Gene...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Mike's Angels</td>
        <td>Leiden University</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">10
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Charles Village</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          JHU CLSP</td>
        <td>Johns Hopkins University</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">11
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Field Lab Beta</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Niels-NTG</td>
        <td>Leiden University</td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
        
    </tbody>
    <tfoot>
      <tr>
        <th scope="row">Average</th>
        <td></td>
        <td></td>
        <td></td>
        

        <td> 0.00 </td>

        

        <td> 0.00 </td>

        

        <td> 0.00 </td>

        

        <td> 0.00 </td>

        

        <td> 0.00 </td>

        
        <td></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
</div>

                </div>
                
                  <div class="tab-pane fade" id="nav-2021" role="tabpanel" aria-labelledby="nav-2021-tab">
                    

  <div class="row">
  <div class="d-flex justify-content-center">
    <a href="https://drive.google.com/file/d/1kPLlVYyRfJf7klF-GzToTB7yO6jSZ6cK/view?usp=sharing" ,="" target="_blank" style="color:gold;">Download the base maps HERE</a>
  </div>
</div>

<div class="row">
<div class="table-responsive">
  <table class="table table-dark table-striped table-bordered align-middle">
    <thead>
      <tr>
        <th scope="col">Entry</th>
        <th scope="col">Generator Name</th>
        <th scope="col">Team Name</th>
        <th scope="col">Affiliation</th>
        
        <th scope="col">
          Adaptability
        </th>
        
        <th scope="col">
          Functionality
        </th>
        
        <th scope="col">
          Narrative
        </th>
        
        <th scope="col">
          Aesthetic
        </th>
        
        <th scope="col">
          Overall
        </th>
        
        <th scope="col">Maps</th>
        <th scope="col">Code</th>
      </tr>
    </thead>
    <tbody>
      
      <tr>
        <td scope="row">1
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">GDMC_2021_TWF_HEIST_v1</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          The World Foundry</td>
        <td>The World Foundry</td>
        
        <td>
          1.66
        </td>
        
        <td>
          3.22
        </td>
        
        <td>
          4.45
        </td>
        
        <td>
          4.31
        </td>
        
        <td>
          3.41
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1SByN6QUYPiTrKesJUs847fYMSRWkh32o/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1LHjZT-ZTJUa_vm6LkL1kYxT3kGpSw29s/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">2
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">ICE_JIT_ft_WFC</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          ICE_JIT_ft_WFC</td>
        <td>Intelligent</td>
        
        <td>
          3.64
        </td>
        
        <td>
          3.68
        </td>
        
        <td>
          4.31
        </td>
        
        <td>
          5.12
        </td>
        
        <td>
          4.19
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1yIdLFmADsqoq-DTWfmDLUjQ-SP0dEG0V/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1ohq647l6kTKLjuE7H5vt03wvbKytYcOn/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">3
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Yeniseigrad</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Rainbow Parliament</td>
        <td>-</td>
        
        <td>
          1.06
        </td>
        
        <td>
          2.65
        </td>
        
        <td>
          3.47
        </td>
        
        <td>
          5.32
        </td>
        
        <td>
          3.13
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1iWEvREVxORHjhScri-0fKqEVccNjZV33/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1fsE40n3A03VKUTcd-kPKr6oTqlC22tJ4/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">4
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">SettlementGeneration</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          William, Selina, Ho Kiu, Rhys</td>
        <td>UniversityOfKent</td>
        
        <td>
          3.91
        </td>
        
        <td>
          5.59
        </td>
        
        <td>
          4.29
        </td>
        
        <td>
          5.71
        </td>
        
        <td>
          4.88
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1j1KM27JXtIslkr2uRqEIALyd0SPCEDjN/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1u7uK-af9DlcNMjhpT4qku1Fi_Kn-Pbmw/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">5
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Chaotic Future Building Comple...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Nils Gawlik</td>
        <td>-</td>
        
        <td>
          3.51
        </td>
        
        <td>
          4.72
        </td>
        
        <td>
          4.99
        </td>
        
        <td>
          6.37
        </td>
        
        <td>
          4.90
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1hJ8I39sQ6V3K33u4kXZbbZs74VCnmRFU/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1JMXkXshqTEscXU5Hk3dLu8NFXn3k_hP7/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">6
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Settlement Generator V1</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Cristopher Yates</td>
        <td>-</td>
        
        <td>
          3.79
        </td>
        
        <td>
          4.24
        </td>
        
        <td>
          4.94
        </td>
        
        <td>
          5.32
        </td>
        
        <td>
          4.57
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/12sOUxvl7molwfGcXBIlPMW-viH4rEzPf/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1k-o9vndhFdfY6ppAgrn5VL8jHV8rMWMR/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">7
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Keywarn's Generator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Keywarn</td>
        <td>University Of Bristol</td>
        
        <td>
          4.07
        </td>
        
        <td>
          2.29
        </td>
        
        <td>
          2.00
        </td>
        
        <td>
          2.97
        </td>
        
        <td>
          2.83
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1P6pLY_OoOqyS6G5owDeSKuTrJVy3VmQE/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/15_wmbO2rjCAPJM-Oo1aPy03eMPoZNJH2/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">8
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">SJC V2</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          LIGC</td>
        <td>-</td>
        
        <td>
          4.90
        </td>
        
        <td>
          3.96
        </td>
        
        <td>
          3.35
        </td>
        
        <td>
          3.99
        </td>
        
        <td>
          4.05
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1B_bankMeFL3GGpCL2L6jQ94J6nmP1DQj/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">9
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Simulation-based village gener...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Lisa</td>
        <td>Maastricht University</td>
        
        <td>
          2.91
        </td>
        
        <td>
          3.37
        </td>
        
        <td>
          3.46
        </td>
        
        <td>
          3.37
        </td>
        
        <td>
          3.28
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1ZEItXEvYf-an21PPeBFtHzqoHCgjuTMX/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/178Q7y4oozmmuAbJrKQp7yIsUmGa2D81-/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">10
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">AgentCraft</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          aith (solo-team)</td>
        <td>n/a</td>
        
        <td>
          4.29
        </td>
        
        <td>
          4.51
        </td>
        
        <td>
          5.27
        </td>
        
        <td>
          5.55
        </td>
        
        <td>
          4.91
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1DHMJskM60Od2l3aLZF5Ebn494GeDpcha/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/12-GP5m_a_kmoloeaD6UWuyFeDnA0Z2sS/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">11
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">PorterHickey</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Porter Hickey</td>
        <td>-</td>
        
        <td>
          3.56
        </td>
        
        <td>
          4.39
        </td>
        
        <td>
          4.03
        </td>
        
        <td>
          6.28
        </td>
        
        <td>
          4.56
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1yaWRiaRwfr3A3OqLKycHxNRVY7MZ83C1/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/199x7h2dNfRhmtmXmetuJG1hC96XQdd5s/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">12
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">NAT AI</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Brianna &amp; Kyle</td>
        <td>-</td>
        
        <td>
          3.65
        </td>
        
        <td>
          4.04
        </td>
        
        <td>
          3.06
        </td>
        
        <td>
          4.92
        </td>
        
        <td>
          3.91
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1l9EJgREBJdESS7Rjd7uVJNlnOjFi1vJd/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1UeMzYrLm1No4aw0IumF0CaREbCLbO2sa/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">13
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Multi Agent Settlement Generat...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          MAU_AE_JF</td>
        <td>Malmo University</td>
        
        <td>
          3.65
        </td>
        
        <td>
          3.06
        </td>
        
        <td>
          2.41
        </td>
        
        <td>
          3.18
        </td>
        
        <td>
          3.07
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/13_G0KGotd_zeo2Gm3jupEGJCaXIc1F50/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1ezKjdPdr7_rAuV1t_am0qts_qNhZwlw7/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">14
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">IRMSG : Immersive and Realist ...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Tsukuba Team</td>
        <td>UTBM</td>
        
        <td>
          4.68
        </td>
        
        <td>
          5.72
        </td>
        
        <td>
          5.60
        </td>
        
        <td>
          5.37
        </td>
        
        <td>
          5.34
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1RExF_NoShHYSOuo4eLZg1Z_3LM23u_BV/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1Hz8UTi9bgkzVVWdxBC1lKtag_7eusG4p/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">15
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">ReXenGen 2021</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Rexos and XeonoX</td>
        <td>-</td>
        
        <td>
          2.65
        </td>
        
        <td>
          2.76
        </td>
        
        <td>
          3.12
        </td>
        
        <td>
          4.38
        </td>
        
        <td>
          3.23
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/12Cl5ATofWU3RWE5OVtqLh-3Zi6hYk0Fm/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1-gFisp3UUlNGnl8wus5QpjsK5eMUMNNk/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">16
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Beautiful_Kaas_Generator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Beautiful_Kaaskoders</td>
        <td>-</td>
        
        <td>
          2.82
        </td>
        
        <td>
          4.71
        </td>
        
        <td>
          4.00
        </td>
        
        <td>
          5.35
        </td>
        
        <td>
          4.22
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1ySmo-oSqgOCKajFMdHwAERqShefn3DsM/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1mKkvWOzikmbZPoS_QAqALhJkLRrSz_nC/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">17
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">VoxArch Grand Castle on a hill...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Hunternif</td>
        <td>-</td>
        
        <td>
          3.18
        </td>
        
        <td>
          1.18
        </td>
        
        <td>
          2.71
        </td>
        
        <td>
          4.09
        </td>
        
        <td>
          2.79
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1w2Rk93eLnEWthMTiKJBIRbJYCXUyZCsF/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1inZVXo1FkyBuLV4lQEEIwVPOI2d36mGD/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">18
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Leifsbu</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Terje Schjelderup</td>
        <td>-</td>
        
        <td>
          4.32
        </td>
        
        <td>
          2.50
        </td>
        
        <td>
          2.63
        </td>
        
        <td>
          2.99
        </td>
        
        <td>
          3.11
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1u_5S7grK6uu4hNs473YiOfftz25vm_nR/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">19
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">DouceFrance</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          CharlieMDRz</td>
        <td>-</td>
        
        <td>
          4.93
        </td>
        
        <td>
          4.43
        </td>
        
        <td>
          4.62
        </td>
        
        <td>
          4.69
        </td>
        
        <td>
          4.67
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1SsvaG6t0lqIeCYZ2IeAa0pTo7qPwX8lD/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1K3-_fIlpIKYSVFDeMtIT2plRBkOA35HK/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">20
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Eixample</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Leiden University MGAI team 1</td>
        <td>Leiden University</td>
        
        <td>
          1.47
        </td>
        
        <td>
          2.21
        </td>
        
        <td>
          3.06
        </td>
        
        <td>
          4.35
        </td>
        
        <td>
          2.77
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/16duCCTBZZ1Qs7V2zp40KJnHX0-5qaXsq/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1-ifc4pUFtsKVOOm-uK0LcKK1xJHrXyuw/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
        
    </tbody>
    <tfoot>
      <tr>
        <th scope="row">Average</th>
        <td></td>
        <td></td>
        <td></td>
        

        <td> 3.27 </td>

        

        <td> 3.49 </td>

        

        <td> 3.61 </td>

        

        <td> 4.46 </td>

        

        <td> 3.71 </td>

        
        <td></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
</div>

                  </div>
                  
                  <div class="tab-pane fade" id="nav-2020" role="tabpanel" aria-labelledby="nav-2020-tab">
                    

  <div class="row">
  <div class="d-flex justify-content-center">
    <a href="https://drive.google.com/file/d/1V3fdRV6plLueVg-RgMxBns8YsqQv1euw/view?usp=sharing" ,="" target="_blank" style="color:gold;">Download the base maps HERE</a>
  </div>
</div>

<div class="row">
<div class="table-responsive">
  <table class="table table-dark table-striped table-bordered align-middle">
    <thead>
      <tr>
        <th scope="col">Entry</th>
        <th scope="col">Generator Name</th>
        <th scope="col">Team Name</th>
        <th scope="col">Affiliation</th>
        
        <th scope="col">
          Adaptability
        </th>
        
        <th scope="col">
          Functionality
        </th>
        
        <th scope="col">
          Narrative
        </th>
        
        <th scope="col">
          Aesthetic
        </th>
        
        <th scope="col">
          Overall
        </th>
        
        <th scope="col">Maps</th>
        <th scope="col">Code</th>
      </tr>
    </thead>
    <tbody>
      
      <tr>
        <td scope="row">1
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Settlevolver</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          The World Foundry</td>
        <td>The World Foundry</td>
        
        <td>
          3.38
        </td>
        
        <td>
          3.19
        </td>
        
        <td>
          5.02
        </td>
        
        <td>
          4.88
        </td>
        
        <td>
          4.11
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1I8u9ydHSwjrME10vPS6mVOSmErMYxAJP/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1oI16cHurokOE3Z2z7APwhwE9HyapbiJ2/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">2
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Train City</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          University of Tsukuba</td>
        <td>University of Tsukuba</td>
        
        <td>
          3.33
        </td>
        
        <td>
          4.92
        </td>
        
        <td>
          4.38
        </td>
        
        <td>
          4.27
        </td>
        
        <td>
          4.22
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1Mv6vFwZX0wlVc188_WEfO-WhNOYxdDV8/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1KJYzmuhEZiT217RH5JdPDWzabOw_hN3N/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">3
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">TFGenerator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Minecrafters</td>
        <td>UCM</td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">4
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">UrbanSettlementGenerator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          maelg</td>
        <td>-</td>
        
        <td>
          3.46
        </td>
        
        <td>
          4.21
        </td>
        
        <td>
          3.65
        </td>
        
        <td>
          4.33
        </td>
        
        <td>
          3.91
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1rQmKRq_MB9-bS5hTOdDMDdL1tg_qQIfc/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">5
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">UrbanSettlementGeneratorV2...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Megacruxis</td>
        <td>-</td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          0.00
        </td>
        
        <td>
          
          <a>n/a</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1el7s6Yqdr2ahkCx5DTfDpsVkdADzi8-D/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">6
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">ICE_JIT</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          ICE_JIT</td>
        <td>Intelligent</td>
        
        <td>
          3.35
        </td>
        
        <td>
          4.13
        </td>
        
        <td>
          4.77
        </td>
        
        <td>
          5.27
        </td>
        
        <td>
          4.38
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1qtmI8c7azU8EkJRnEBAm0RrzBAZ5DgLa/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/18iJcYKv6n3SDLCaQLq0KzTe2WkZoF7dZ/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">7
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Architectural Profiles Iterati...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Architectural Profiles</td>
        <td>Delft University of Technology</td>
        
        <td>
          4.63
        </td>
        
        <td>
          5.60
        </td>
        
        <td>
          4.50
        </td>
        
        <td>
          4.90
        </td>
        
        <td>
          4.91
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1lcjgFciXCWpFRjgD2-vN62qN57l0LVTT/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">8
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">MyVeryKewlSettlementGeneratorV...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          David Mason</td>
        <td>-</td>
        
        <td>
          3.90
        </td>
        
        <td>
          4.85
        </td>
        
        <td>
          4.29
        </td>
        
        <td>
          4.65
        </td>
        
        <td>
          4.42
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1KSCanHACHsCz288mgodWgeZ_-lZ3YYM5/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1lVUHBibnWSWRdyLsIgqpO_rcrB6et5hn/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">9
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">The Charretiers</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          The Charretiers</td>
        <td>-</td>
        
        <td>
          3.65
        </td>
        
        <td>
          4.17
        </td>
        
        <td>
          3.75
        </td>
        
        <td>
          3.83
        </td>
        
        <td>
          3.85
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1NDbyNKtvY2HV4b08M_2XPmGqTTeWAP3g/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
      <tr>
        <td scope="row">10
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">MUNGEN V1.0.1</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Troy, Ryan, &amp; Trent</td>
        <td>-</td>
        
        <td>
          4.63
        </td>
        
        <td>
          5.60
        </td>
        
        <td>
          4.50
        </td>
        
        <td>
          4.90
        </td>
        
        <td>
          4.91
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1HyXGMws2KZRi6tD2XSdwTOJVJ83BsWU-/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a>n/a</a>
          
        </td>
      </tr> 
        
    </tbody>
    <tfoot>
      <tr>
        <th scope="row">Average</th>
        <td></td>
        <td></td>
        <td></td>
        

        <td> 2.76 </td>

        

        <td> 3.33 </td>

        

        <td> 3.17 </td>

        

        <td> 3.37 </td>

        

        <td> 3.16 </td>

        
        <td></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
</div>

                  </div>
                  
                  <div class="tab-pane fade" id="nav-2019" role="tabpanel" aria-labelledby="nav-2019-tab">
                    

  <div class="row">
  <div class="d-flex justify-content-center">
    <a href="https://drive.google.com/file/d/18B8IQduF0xl43EpsAMeJ9IJrM486akRH/view?usp=sharing" ,="" target="_blank" style="color:gold;">Download the base maps HERE</a>
  </div>
</div>

<div class="row">
<div class="table-responsive">
  <table class="table table-dark table-striped table-bordered align-middle">
    <thead>
      <tr>
        <th scope="col">Entry</th>
        <th scope="col">Generator Name</th>
        <th scope="col">Team Name</th>
        <th scope="col">Affiliation</th>
        
        <th scope="col">
          Adaptability
        </th>
        
        <th scope="col">
          Functionality
        </th>
        
        <th scope="col">
          Narrative
        </th>
        
        <th scope="col">
          Aesthetic
        </th>
        
        <th scope="col">
          Overall
        </th>
        
        <th scope="col">Maps</th>
        <th scope="col">Code</th>
      </tr>
    </thead>
    <tbody>
      
      <tr>
        <td scope="row">1
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Delegated generation procedura...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Adrian</td>
        <td>The World Foundry</td>
        
        <td>
          2.82
        </td>
        
        <td>
          3.36
        </td>
        
        <td>
          3.91
        </td>
        
        <td>
          3.91
        </td>
        
        <td>
          3.50
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1WZDlGi05_H2jWIdhEF8nb1KlfZcXwJpo/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/19jRqunPUP6kYVKSDxK8py_iGR1rW-_Rq/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">2
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Incremental Bottom-Up Settleme...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Filip</td>
        <td>-</td>
        
        <td>
          5.82
        </td>
        
        <td>
          5.18
        </td>
        
        <td>
          4.91
        </td>
        
        <td>
          5.73
        </td>
        
        <td>
          5.50
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/18jUoe2IZw_SsPrgFcTpX4i9Lro9Cg3oO/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1LmL3P7fHdIgOWxA02-4TulKzof2qM6CN/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">3
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">UrbanSettlementGenerator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          ehauckdo</td>
        <td>University of Tsukuba</td>
        
        <td>
          3.09
        </td>
        
        <td>
          4.27
        </td>
        
        <td>
          3.73
        </td>
        
        <td>
          4.45
        </td>
        
        <td>
          3.95
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1Va36d3dWkx0LVJGH1eVZaHX2eatsxSQ1/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1V5vmlSxoV1LDpvMG9cXgRF2n6f6HogdR/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">4
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Big Lumberboi</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Julos14</td>
        <td>University of Southern Denmark</td>
        
        <td>
          5.45
        </td>
        
        <td>
          5.00
        </td>
        
        <td>
          5.00
        </td>
        
        <td>
          5.91
        </td>
        
        <td>
          5.39
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1zT8BMmSThtmrpb31nkbKOJvKp7wru3fc/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1KpZ-Rkt2cFTejWILoQqF9P3rb9StImw7/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">5
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">SettlementGenerator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          ArtCodeOutdoors</td>
        <td>None</td>
        
        <td>
          5.09
        </td>
        
        <td>
          4.45
        </td>
        
        <td>
          4.73
        </td>
        
        <td>
          5.73
        </td>
        
        <td>
          4.95
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1x4a59718b7yDpvXsT7X6EYRAOHqB_Bq7/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1XH7GaC7JIfI1T5eSsBDrRJxVNM9Op_f_/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">6
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">settlements-0.1.0</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Berlier</td>
        <td>-</td>
        
        <td>
          4.36
        </td>
        
        <td>
          4.18
        </td>
        
        <td>
          4.27
        </td>
        
        <td>
          5.55
        </td>
        
        <td>
          4.70
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1HDdScr-Z-JDvfpkSc8_X9fJfS4OG4ASk/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1-IsUZFiXHLQh55-9h75-AscHZlR8eBU3/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
        
    </tbody>
    <tfoot>
      <tr>
        <th scope="row">Average</th>
        <td></td>
        <td></td>
        <td></td>
        

        <td> 3.80 </td>

        

        <td> 3.78 </td>

        

        <td> 3.79 </td>

        

        <td> 4.47 </td>

        

        <td> 4.00 </td>

        
        <td></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
</div>

                  </div>
                  
                  <div class="tab-pane fade active show" id="nav-2018" role="tabpanel" aria-labelledby="nav-2018-tab">
                    

  <div class="row">
  <div class="d-flex justify-content-center">
    <a href="https://drive.google.com/file/d/1Hc9OmfmsQ4GUC_lHtIwRvMsvSsO1uaBr/view?usp=sharing" ,="" target="_blank" style="color:gold;">Download the base maps HERE</a>
  </div>
</div>

<div class="row">
<div class="table-responsive">
  <table class="table table-dark table-striped table-bordered align-middle">
    <thead>
      <tr>
        <th scope="col">Entry</th>
        <th scope="col">Generator Name</th>
        <th scope="col">Team Name</th>
        <th scope="col">Affiliation</th>
        
        <th scope="col">
          Adaptability
        </th>
        
        <th scope="col">
          Functionality
        </th>
        
        <th scope="col">
          Narrative
        </th>
        
        <th scope="col">
          Aesthetic
        </th>
        
        <th scope="col">
          Overall
        </th>
        
        <th scope="col">Maps</th>
        <th scope="col">Code</th>
      </tr>
    </thead>
    <tbody>
      
      <tr>
        <td scope="row">0
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Incremental bottom-up settleme...</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Filip</td>
        <td>-</td>
        
        <td>
          5.42
        </td>
        
        <td>
          4.71
        </td>
        
        <td>
          3.17
        </td>
        
        <td>
          4.21
        </td>
        
        <td>
          4.38
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/16yXn1Kc9WydpuCL67bSLVhK0DqRm1eWi/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1ZBZqk7CTjc-F6YwFeF5uzQsaLlaNo1JV/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">1
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">ABODE</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Adrian</td>
        <td>The World Foundry</td>
        
        <td>
          2.33
        </td>
        
        <td>
          2.21
        </td>
        
        <td>
          2.13
        </td>
        
        <td>
          3.54
        </td>
        
        <td>
          2.55
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1tUsUk8LZ_tqJa7MHaswWvodHtAqM-O_T/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1FsAGuGTiGtumSQrarYRY_w6AOuhoa_Tc/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">2
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">Settlement Generator</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Rafael</td>
        <td>-</td>
        
        <td>
          3.25
        </td>
        
        <td>
          3.25
        </td>
        
        <td>
          2.46
        </td>
        
        <td>
          3.79
        </td>
        
        <td>
          3.08
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/1NKu3GPpb60qa-_gmM4xvQGjOOS51IMrS/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/16C56qQlpsB6mTEhhUdchwZHNhluPRD-O/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
      <tr>
        <td scope="row">3
        </td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">HouseAndRoadBuilder</td>
        <td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">
          Changxing &amp; Shaofang</td>
        <td>-</td>
        
        <td>
          0.96
        </td>
        
        <td>
          2.96
        </td>
        
        <td>
          2.13
        </td>
        
        <td>
          2.75
        </td>
        
        <td>
          2.20
        </td>
        
        <td>
          
          <a href="https://drive.google.com/file/d/13ROspmaggf8e_thpngKBtmM7K39108Gg/view?usp=sharing" target="_blank" style="color:gold;">maps</a>
          
          </td>
        <td>
        
          <a href="https://drive.google.com/file/d/1_5RjwAHlMSvA3MDyEUP9xQDNqhO3AOUo/view?usp=sharing" target="_blank" style="color:gold;">code</a>
        
        </td>
      </tr> 
        
    </tbody>
    <tfoot>
      <tr>
        <th scope="row">Average</th>
        <td></td>
        <td></td>
        <td></td>
        

        <td> 2.99 </td>

        

        <td> 3.28 </td>

        

        <td> 2.47 </td>

        

        <td> 3.57 </td>

        

        <td> 3.05 </td>

        
        <td></td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
</div>

                  </div>
                  
            </div>
          </div>
"""

rows = [x.strip() for x in data.split('\n')]

years = ['', '2021', '2020', '2019', '2018']

current_year = years[0]
current_team = ''
for row in rows:
    if row.startswith('</td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">'):
        current_team = row[len('</td><td style="word-wrap: break-word;min-width: 160px;max-width: 160px;">'):-5]
        if '...' in current_team:
            current_team = current_team[:-3]
        current_team = current_team.replace(':', '-').strip()
    if row.startswith('<a href="'):
        link = row[9:row.index('"', 10)]
        if link == '/':
            continue

        link_id = link[len('https://drive.google.com/file/d/'):-len('/view?usp=sharing')]
        download_link = f'https://drive.google.com/u/0/uc?id={link_id}&export=download&confirm=t'

        if 'Download the base maps HERE' in row:
            current_year = years[years.index(current_year) + 1]
            print(f'Download Maps for {current_year} from {download_link}')
            path = f'past-code/{current_year}/maps'
        elif 'maps' in row:
            print(f'Download Maps for {current_team} from {download_link}')
            path = f'past-code/{current_year}/{current_team}/maps'
        elif 'code' in row:
            print(f'Download Code for {current_team} from {download_link}')
            path = f'past-code/{current_year}/{current_team}/src'
        else:
            continue
        try:
            makedirs(path)
        except FileExistsError:
            continue
        urllib.request.urlretrieve(download_link, join(path, 'download.zip'))
        try:
            with zipfile.ZipFile(join(path, 'download.zip'), "r") as zip_ref:
                zip_ref.extractall(path)

        except zipfile.BadZipfile:
            continue
        finally:
            remove(join(path, 'download.zip'))