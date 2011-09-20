#!/bin/bash

( cd fleet-info; ./randgen fleetinfo.txt )
cat fleet-info/*AAL-ac.conf American-Airlines/american_airlines_flights.conf > xmltools/AAL.conf
cat fleet-info/*BAW-ac.conf ./Oneworld/airlines/BAW.conf                     > xmltools/BAW.conf
cat fleet-info/*UAL-ac.conf ./Continental/airlines/UAL.conf                  > xmltools/UAL.conf
cat fleet-info/*DAL-ac.conf ./SkyTeam/airlines/DAL.conf                      > xmltools/DAL.conf

cd xmltools
./conf2xml.pl

for letter in A B D U; do
    mv ${letter}??.xml ~/src/flightgear-git/fgdata/AI/Traffic/${letter}
done;

