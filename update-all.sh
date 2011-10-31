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

cd xmltools
./conf2xml.pl

for letter in A B C D I Q S U; do
    mv ${letter}??.xml ~/src/flightgear-git/fgdata/AI/Traffic/${letter}
done;


