#!/usr/bin/perl -w


sub parseTime {
   #print "Parsing time @_";
   #die;
   my $timeStr = @_[0];
   @timeArray = split(":", $timeStr);
   #print STDERR @timeArray, "\n";
   return ($timeArray[0] + $timeArray[1]/60.0);
}

@inputfiles = glob("???.conf");

while ($infile = shift(@inputfiles)) {
    open (CONF, $infile) or die "Unable to open input configuration file";
    ($outname = $infile) =~ s/conf/xml/;
    print "Writing to $outname\n";
    open XMLFILE, ">$outname";
    while ($buf = readline(CONF)) {
    

    push @DataList, $buf;
    }
    close (CONF);
    print XMLFILE "<?xml version=\"1.0\"?>\n";
    print XMLFILE "<trafficlist>\n";
    while ($dataline = shift(@DataList)) {
        @tokens = split(" ", $dataline);
        if (scalar(@tokens) > 0) {
            if ($tokens[0] eq "AC") {
                #print XMLFILE @tokens, "\n";
                print XMLFILE "    <aircraft>\n";
                print XMLFILE "        <model>$tokens[12]</model>\n";
                print XMLFILE "        <livery>$tokens[6]</livery>\n";
                print XMLFILE "        <airline>$tokens[5]</airline>\n";
                print XMLFILE "        <home-port>$tokens[1]</home-port>\n";
                print XMLFILE "        <required-aircraft>$tokens[3]-$tokens[5]</required-aircraft>\n";
                print XMLFILE "        <actype>$tokens[4]</actype>\n";
                print XMLFILE "        <offset>$tokens[7]</offset>\n";
                print XMLFILE "        <radius>$tokens[8]</radius>\n";
                print XMLFILE "        <flighttype>$tokens[9]</flighttype>\n";
                print XMLFILE "        <performance-class>$tokens[10]</performance-class>\n";
                print XMLFILE "        <registration>$tokens[2]</registration>\n";
                print XMLFILE "        <heavy>$tokens[11]</heavy>\n";
                print XMLFILE "    </aircraft>\n";
            }
            if ($tokens[0] eq "FLIGHT") {
                $weekdays = $tokens[3];
                @days = split(//, $weekdays);
                if (1) {
                    for ($i = 0; $i < 7; $i++) {
                        #print XMLFILE " $days[$i]";
                        if (!(($days[$i] eq $i) || ($days[$i] eq "."))) { die "invalid weekday $tokens[3]" };
    
                        $depTime = parseTime($tokens[4]);
                        $arrTime = parseTime($tokens[6]);
                        $depDay = $i + 1;
                        if ($depDay > 6) {
                            $depDay = 0;
                        }
    
                        $arrDay = $depDay;
                        if ($depTime > $arrTime) {
                            $arrDay++;
                        }
                        if ($arrDay > 6) {
                            $arrDay = 0;
                        }
                        if ($days[$i] eq $i) {
                            print XMLFILE "        <flight>\n";
                            print XMLFILE "            <callsign>$tokens[1]</callsign>\n";
                            print XMLFILE "            <required-aircraft>$tokens[9]</required-aircraft>\n";
                            print XMLFILE "            <fltrules>$tokens[2]</fltrules>\n";
                            print XMLFILE "            <departure>\n";
                            print XMLFILE "                <port>$tokens[5]</port>\n";
                            print XMLFILE "                <time>$depDay/$tokens[4]:00</time>\n";
                            print XMLFILE "            </departure>\n";
                            print XMLFILE "            <cruise-alt>$tokens[8]</cruise-alt>\n";
                            print XMLFILE "            <arrival>\n";
                            print XMLFILE "                <port>$tokens[7]</port>\n";
                            print XMLFILE "                <time>$arrDay/$tokens[6]:00</time>\n";
                            print XMLFILE "            </arrival>\n";
                            print XMLFILE "            <repeat>WEEK</repeat>\n";
                            print XMLFILE "        </flight>\n";
                        }
                }
                } else {
                    print XMLFILE "        <flight>\n";
                    print XMLFILE "            <callsign>$tokens[1]</callsign>\n";
                    print XMLFILE "            <required-aircraft>$tokens[9]</required-aircraft>\n";
                    print XMLFILE "            <fltrules>$tokens[2]</fltrules>\n";
                    print XMLFILE "            <departure>\n";
                    print XMLFILE "                <port>$tokens[5]</port>\n";
                    print XMLFILE "                <time>$tokens[4]:00</time>\n";
                    print XMLFILE "            </departure>\n";
                    print XMLFILE "            <cruise-alt>$tokens[8]</cruise-alt>\n";
                    print XMLFILE "            <arrival>\n";
                    print XMLFILE "                <port>$tokens[7]</port>\n";
                    print XMLFILE "                <time>$tokens[6]:00</time>\n";
                    print XMLFILE "            </arrival>\n";
                    print XMLFILE "            <repeat>24Hr</repeat>\n";
                    print XMLFILE "        </flight>\n";
                }
            }
        }
    }
    print XMLFILE "</trafficlist>\n";
    close XMLFILE;
}
