#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <boost/algorithm/string.hpp>

#include <stdio.h>

// open a text file containing the fleet requirements. 

using namespace std;

vector<string> callsigns;
vector<string>::iterator it;

string randomSelectHomeport(string in) {
    vector<string> strs;
    boost::split(strs, in, boost::is_any_of(","));
    //cerr << "split string into" << strs.size() << "pieces" << endl;
    return strs[rand() % strs.size()];
}

string generateCallSign(string in) {
    string result;
    char buffer[128];
    for (int i = 0; i < in.size(); i++) {
        if (in[i] != '\%') {
            result = result + in[i];
        } else {
            i++;
            if ((in[i] == 'd') || (in[i] == 's')) {
                if (in[i] == 'd') {
                    snprintf(buffer, 128, "%d", rand() % 10);
                }
                if (in[i] == 's') {
                    char x = 'A' + rand() % 26;
                    //cerr << "using token " << x << endl;
                    snprintf(buffer, 128, "%c", x);
                }
            } else {
                cerr << "Unknown token " << in[i] << " in callsign format " << in << endl;
                exit(1);
            }
            result = result + buffer;
        }
    }
    //cerr << "returning callsign" << result << endl;
    return result;
}

bool exists(string in) {
    for (it = callsigns.begin(); it != callsigns.end(); it++) {
        if ((*it) == in) {
            return true;
        }
    }
    return false;
}


string generateUniqueCallSign(string in) {
    string result;
    do {
        result = generateCallSign(in);
    } while (exists(result));
    callsigns.push_back(result);
    return result;
}


int main(int argc, char *argv[]) {
    if (argc < 2) {
        cerr << "Usage : " << argv[0] << "[ fleetinfofile ] " << endl;
        exit(1);
    } 
    ifstream fleetinfo(argv[1]);
    if (!fleetinfo.is_open()) {
        cerr << "error opening file : " << argv[1] << endl;
    }
    while (1) {
        char buffer[128];
        fleetinfo.getline(buffer, 128);
        if (fleetinfo.eof()) {
            break;
        }
        string line(buffer);
        string dum, airline, actypedef, numberstring, homeports, tailNumberTemplate, callsign;
        cerr << "Processing line : " << line <<endl;
        if (line.find(string("ENTRY")) != string::npos) {
            istringstream iss(line);
            iss >> dum;
            iss >> airline;
            iss >> actypedef;
            iss >> numberstring;
            iss >> homeports;
            iss >> tailNumberTemplate;
            iss >> callsign;
            /*cerr << " " << dum 
                << " " << airline
                << " " << actypedef
                << " " << numberstring
                << " " << homeports
                << " " << callsigntemplate << endl;
                */
            ifstream accodes("aircraft.txt");
            string origcode, newcode;
            string acdata;
            while (1) {
                accodes >> origcode >> newcode;
                char buffer[128];
                accodes.getline(buffer, 128);
                acdata = string(buffer);
                //cerr << "Buffer = " << buffer << endl;
                if (accodes.eof()) {
                    cerr << "Error: Aircraft code " << actypedef << " not found in aircraft.txt" << endl;
                    exit(1);
                }
                if (origcode == actypedef) {
                    if (acdata.empty()) {
                        cerr << "Aircraft information not found for " << origcode << endl;
                        exit(1);
                    }
                    break;
                }
            }
            //string acdefFilename = newcode + ".txt";
            //ifstream acdef(acdefFilename.c_str());
            //cerr << "Opening " << acdefFilename << endl;
            //
            //if (acdef.is_open()) {
            //    cerr << "Parsing contents of " << acdefFilename << endl;
            //    char buffer[128];
            //    acdef.getline(buffer, 128);
            //    acdata = string(buffer);
            //} else {
            //    cerr << "Error opening " << acdefFilename << endl;
            //    exit(1);
            //}
            int nrAircraft = atoi(numberstring.c_str());
            string acfilename = origcode + "-" + airline + "-ac.conf";
            ofstream acfile(acfilename.c_str());
            for (int i = 0; i < nrAircraft; i++) {
                string homeport = randomSelectHomeport(homeports);
                string tailnumber = generateUniqueCallSign(tailNumberTemplate);
                acfile << "AC " 
                    << homeport
                    << " " << tailnumber
                    << " " << origcode 
                    << " " << origcode
                    << " " << airline 
                    << " " << airline
                    << " " << acdata
                    << callsign << ".xml" << endl;
            }
        }
    }
    return 0;
}
