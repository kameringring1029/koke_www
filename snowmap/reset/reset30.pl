#!/usr/bin/perl

use File::Copy 'copy';
use File::Remove qw(remove);

$dir = "/var/www/snowmap/log";

$gfile = "$dir/counter/gcounter.dat";
$gfile30 = "$dir/counter/gcounter30.dat";
$sfile = "$dir/counter/scounter.dat";
$wfile = "$dir/counter/countlog30/countlog30.csv";


#現在時刻取得
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


#ファイルから各カウンタ値取得
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


#30分間をまとめてファイルに書きこみ
if(open(OUT,">> $wfile")){
  flock(OUT,2);
  print OUT "$year/$mon/$mday $hour:$min:$sec,<gen>$gcount,<gen30>$gcount30,<spc>$scount\n";
  close(OUT);
}else{
print "write error\n";
}


#30分カウンタをリセット
remove "$dir/counter/gcounter30.dat";
copy "$dir/counter/reset.dat" ,"$dir/counter/gcounter30.dat";
chmod 0777 ,"$dir/counter/gcounter30.dat";

