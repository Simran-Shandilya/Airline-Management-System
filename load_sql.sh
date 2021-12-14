#!/bin/sh

cat ./AIRPORTS.csv | psql -U pk2460 -d pk2460_db -c "COPY airport from STDIN CSV HEADER"
cat ./AIRPLANE_AIRLINE.csv | psql -U pk2460 -d pk2460_db -c "COPY airplane_airline from STDIN CSV HEADER"
cat ./STOP.csv | psql -U pk2460 -d pk2460_db -c "COPY stop from STDIN CSV HEADER"
cat ./FLIGHT_TRIP.csv | psql -U pk2460 -d pk2460_db -c "COPY flight_trip from STDIN CSV HEADER"
cat ./SEAT.csv | psql -U pk2460 -d pk2460_db -c "COPY seat from STDIN CSV HEADER"
cat ./FARE.csv | psql -U pk2460 -d pk2460_db -c "COPY fare from STDIN CSV HEADER"
cat ./TRAVELLER.csv | psql -U pk2460 -d pk2460_db -c "COPY traveller from STDIN CSV HEADER"
cat ./USERS.csv | psql -U pk2460 -d pk2460_db -c "COPY users from STDIN CSV HEADER"
