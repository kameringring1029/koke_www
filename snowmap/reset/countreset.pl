#!/usr/bin/perl

$gfile="/var/www/snowmap/log/counter/gcounter.dat";
$gfile30="/var/www/snowmap/log/counter/gcounter30.dat";
$sfile="/var/www/snowmap/log/counter/scounter.dat";
$wfile="/var/www/snowmap/log/counter/countlog.csv";
$file30="/var/www/snowmap/log/counter/countlog30/countlog30.csv";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year+=1900;
$mon+=1;
#２ケタ統一
if(length($mon) == 1){
  $mon = "0$mon";
}
if(length($mday) == 1){
  $mday = "0$mday";
}


#各カウンタ値をファイルから取得
if(open(FH, $gfile)){
  eval{flock(FH, 2);};
  $gcount = <FH>;
    chomp($gcount);
  close(FH);
}else{
  print"gread error\n";
}
if(open(FH, $gfile30)){
  eval{flock(FH, 2);};
  $gcount30 = <FH>;
    chomp($gcount30);
  close(FH);
}else{
  print"g30read error\n";
}
if(open(FH, $sfile)){
  eval{flock(FH, 2);};
  $scount = <FH>;
    chomp($scount);
  close(FH);
}else{
  print"sread error\n";
}


#一日分をまとめてファイルに書き込み
if(open(OUT,">> $wfile")){
  flock(OUT,2);
  print OUT "$year/$mon/$mday $hour:$min:$sec,<gen>$gcount,<gen30>$gcount30,<spc>$scount\n";
  close(OUT);
}else{
print "write error\n";
}


