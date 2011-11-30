#!/bin/bash

( cd fleet-info; ./randgen fleetinfo.txt )
cat fleet-info/*AAL-ac.conf ./American-Airlines/american_airlines_flights.conf > xmltools/AAL.conf
cat fleet-info/*BAW-ac.conf ./Oneworld/airlines/BAW.conf                       > xmltools/BAW.conf
cat fleet-info/*UAL-ac.conf ./Continental/airlines/UAL.conf                    > xmltools/UAL.conf
cat fleet-info/*DAL-ac.conf ./SkyTeam/airlines/DAL.conf                        > xmltools/DAL.conf
cat fleet-info/*COA-ac.conf ./StarAlliance/airlines/COA.conf                   > xmltools/COA.conf
cat fleet-info/*USA-ac.conf ./StarAlliance/airlines/USA.conf                   > xmltools/USA.conf
cat fleet-info/*DLH-ac.conf ./StarAlliance/airlines/DLH.conf                   > xmltools/DLH.conf
cat fleet-info/*IBE-ac.conf ./Oneworld/airlines/IBE.conf                       > xmltools/IBE.conf
cat fleet-info/*SAS-ac.conf ./StarAlliance/airlines/SAS.conf                   > xmltools/SAS.conf
cat fleet-info/*ACA-ac.conf ./StarAlliance/airlines/ACA.conf                   > xmltools/ACA.conf
cat fleet-info/*AFR-ac.conf ./AirFrance/airfrance_flights.conf                 > xmltools/AFR.conf
cat fleet-info/*AZA-ac.conf ./Alitalia/alitalia_flights.conf                   > xmltools/AZA.conf
cat fleet-info/*QFA-ac.conf ./Oneworld/airlines/QFA.conf                       > xmltools/QFA.conf
cat fleet-info/*TAP-ac.conf ./StarAlliance/airlines/TAP.conf                   > xmltools/TAP.conf
cat fleet-info/*ASA-ac.conf ./SkyTeam/airlines/ASA.conf                        > xmltools/ASA.conf
cat fleet-info/*LAN-ac.conf ./Oneworld/airlines/LAN.conf                       > xmltools/LAN.conf
cat fleet-info/*FIN-ac.conf ./Oneworld/airlines/FIN.conf                       > xmltools/FIN.conf
cat fleet-info/*SWR-ac.conf ./StarAlliance/airlines/SWR.conf                   > xmltools/SWR.conf
cat fleet-info/*JKK-ac.conf ./StarAlliance/airlines/JKK.conf                   > xmltools/JKK.conf

cat fleet-info/*THY-ac.conf ./StarAlliance/airlines/THY.conf                   > xmltools/THY.conf
cat fleet-info/*CCA-ac.conf ./StarAlliance/airlines/CCA.conf                   > xmltools/CCA.conf
cat fleet-info/*ROT-ac.conf /Tarom/tarom_flights.conf                          > xmltools/ROT.conf
cat fleet-info/*TAM-ac.conf ./StarAlliance/airlines/TAM.conf                   > xmltools/TAM.conf
cat fleet-info/*ANZ-ac.conf ./StarAlliance/airlines/ANZ.conf                   > xmltools/ANZ.conf
cat fleet-info/*JAL-ac.conf ./Oneworld/airlines/JAL.conf                       > xmltools/JAL.conf
cat fleet-info/*ANA-ac.conf ./StarAlliance/airlines/ANA.conf                   > xmltools/ANA.conf
cat fleet-info/*MSR-ac.conf ./StarAlliance/airlines/MSR.conf                   > xmltools/MSR.conf
cat fleet-info/*DAT-ac.conf ./StarAlliance/airlines/DAT.conf                   > xmltools/DAT.conf
cat fleet-info/*CSA-ac.conf ./SkyTeam/airlines/CSA.conf                        > xmltools/CSA.conf
cat fleet-info/*SBI-ac.conf ./Oneworld/airlines/SBI.conf                       > xmltools/SBI.conf
cat fleet-info/*RJA-ac.conf ./Oneworld/airlines/RJA.conf                       > xmltools/RJA.conf
cat fleet-info/*BMA-ac.conf ./StarAlliance/airlines/BMA.conf                   > xmltools/BMA.conf
cat fleet-info/*LOT-ac.conf ./StarAlliance/airlines/LOT.conf                   > xmltools/LOT.conf
cat fleet-info/*CTN-ac.conf ./StarAlliance/airlines/CTN.conf                   > xmltools/CTN.conf
cat fleet-info/*CPA-ac.conf ./Oneworld/airlines/CPA.conf                       > xmltools/CPA.conf
cat fleet-info/*AUA-ac.conf ./StarAlliance/airlines/AUA.conf                   > xmltools/AUA.conf
cat fleet-info/*AEE-ac.conf ./StarAlliance/airlines/AEE.conf                   > xmltools/AEE.conf
cat fleet-info/*THA-ac.conf ./StarAlliance/airlines/THA.conf                   > xmltools/THA.conf
cat fleet-info/*MAH-ac.conf ./Oneworld/airlines/MAH.conf                       > xmltools/MAH.conf
cat fleet-info/*SQC-ac.conf ./StarAlliance/airlines/SQC.conf                   > xmltools/SQC.conf
cat fleet-info/*SAA-ac.conf ./StarAlliance/airlines/SAA.conf                   > xmltools/SAA.conf
cat fleet-info/*AMX-ac.conf ./SkyTeam/airlines/AMX.conf                        > xmltools/AMX.conf
cat fleet-info/*ADR-ac.conf ./StarAlliance/airlines/ADR.conf                   > xmltools/ADR.conf
cat fleet-info/*HDA-ac.conf ./Oneworld/airlines/HDA.conf                       > xmltools/HDA.conf
cat fleet-info/*BLF-ac.conf ./StarAlliance/airlines/BLF.conf                   > xmltools/BLF.conf
cat fleet-info/*KAL-ac.conf ./SkyTeam/airlines/KAL.conf                        > xmltools/KAL.conf
cat fleet-info/*HAL-ac.conf ./SkyTeam/airlines/HAL.conf                        > xmltools/HAL.conf
cat fleet-info/*TAO-ac.conf ./Continental/airlines/TAO.conf                    > xmltools/TAO.conf
cat fleet-info/*JTA-ac.conf ./Oneworld/airlines/JTA.conf                       > xmltools/JTA.conf
cat fleet-info/*GLO-ac.conf ./SkyTeam/airlines/GLO.conf                        > xmltools/GLO.conf
cat fleet-info/*CMP-ac.conf ./Continental/airlines/CMP.conf                    > xmltools/CMP.conf
cat fleet-info/*KAP-ac.conf ./Continental/airlines/KAP.conf                    > xmltools/KAP.conf
cat fleet-info/*LOF-ac.conf ./Continental/airlines/LOF.conf                    > xmltools/LOF.conf
cat fleet-info/*LNE-ac.conf ./Oneworld/airlines/LNE.conf                       > xmltools/LNE.conf
cat fleet-info/*MKU-ac.conf ./Continental/airlines/NKU.conf                    > xmltools/MKU.conf
cat fleet-info/*OAL-ac.conf ./SkyTeam/airlines/OAL.conf                        > xmltools/OAL.conf
cat fleet-info/*VIR-ac.conf ./Continental/airlines/VIR.conf                    > xmltools/VIR.conf
cat fleet-info/*DSM-ac.conf ./Oneworld/airlines/DSM.conf                       > xmltools/DSM.conf
cat fleet-info/*LPE-ac.conf ./Oneworld/airlines/LPE.conf                       > xmltools/LPE.conf


cd xmltools
./conf2xml.pl

for letter in A B C D F G H I J K L M O Q R S T U V; do
    mv ${letter}??.xml ~/src/flightgear-git/fgdata/AI/Traffic/${letter}
done;


