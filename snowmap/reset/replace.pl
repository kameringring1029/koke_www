#!/usr/bin/perl
use strict;
use utf8;

#日付変更時、当日分ログファイルを
#日付毎ファイルに置き換えるPerl

use File::Copy 'copy';

#ログディレクトリ
my $dir = "/var/www/snowmap/log";
#観測地の数
my $locnum = 7;

my $ln = "\x0A";


#元ファイル指定
my $sfile="$dir/hourfall/hourfall.csv";
my $afile="$dir/counter/acclog/acclog.csv";
my $cfile="$dir/counter/countlog30/countlog30.csv";

my @sc = {};
my @the = {};
my @raw = {};
my @pho = {};
for(my $c=1;$c<=$locnum;$c++){
  $sc[$c] = "$dir/snowcover/cover$c.csv";
  $the[$c]="$dir/thermo/thermo$c.csv";
  $raw[$c]="$dir/rawdata/rawdata$c.csv";
  $pho[$c]="$dir/photo/loc$c/today/";
}
my $scA="$dir/snowcover/covers.csv";
my $theA="$dir/thermo/thermos.csv";


#ディレクトリ指定
my $sdir="$dir/hourfall/";
my $adir="$dir/counter/acclog/";
my $cdir="$dir/counter/countlog30/";

my @scdir = {};
my @thedir = {};
my @rawdir = {};
my @phodir = {};
for(my $c=1;$c<=$locnum;$c++){
  $scdir[$c]="$dir/snowcover/loc$c/";
  $thedir[$c]="$dir/thermo/loc$c/";
  $rawdir[$c]="$dir/rawdata/loc$c/";
  $phodir[$c]="$dir/photo/loc$c/";
}
my $scdirA="$dir/snowcover/locAll/";
my $thedirA="$dir/thermo/locAll/";


#現在時刻取得
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year+=1900;
$mon+=1;
#前日データなので日付を前日に
if($mday eq "1"){$mday = "32";}
$mday-=1;
#２ケタ統一
if(length($mon) == 1){
  $mon = "0$mon";
}
if(length($mday) == 1){
  $mday = "0$mday";
}

my $times="$year-$mon-$mday";


#変更先ファイル名指定
my $stime="$sdir$year-$mon-$mday.csv";
my $atime="$adir$year-$mon-$mday.csv";
my $ctime="$cdir$year-$mon-$mday.csv";

my @sctime = {};
my @thetime = {};
my @rawtime = {};
my @photime = {};
for(my $c=1;$c<=$locnum;$c++){
  $sctime[$c]="$scdir[$c]$times.csv";
  $thetime[$c]="$thedir[$c]$times.csv";
#  $rawtime[$c]="$rawdir[$c]$times";
  $rawtime[$c]="$rawdir[$c]$times.csv";
  $photime[$c]="$phodir[$c]$times";
}
my $sctimeA="$scdirA$times.csv";
my $thetimeA="$thedirA$times.csv";


#置き換え
rename $sfile, $stime;
rename $afile, $atime;
rename $cfile, $ctime;

for(my $c=1;$c<=$locnum;$c++){
  rename $sc[$c], $sctime[$c];
  rename $the[$c], $thetime[$c];
  rename $raw[$c], $rawtime[$c];
  rename $pho[$c], $photime[$c];
}

copy $scA, $sctimeA;
copy $theA, $thetimeA;


#翌日分ファイルを作成
copy "$dir/hourfall/.reset.csv" ,"$dir/hourfall/hourfall.csv";
copy "$dir/counter/countlog30/reset.csv" ,"$dir/counter/countlog30/countlog30.csv";
copy "$dir/counter/acclog/reset.csv" ,"$dir/counter/acclog/acclog.csv";

for(my $c=1;$c<=$locnum;$c++){
  copy "$dir/snowcover/reset.csv" ,"$dir/snowcover/cover$c.csv";
  chmod 0777 ,"$dir/snowcover/cover$c.csv";
}

for(my $c=1;$c<=$locnum;$c++){
  copy "$dir/thermo/reset.csv" ,"$dir/thermo/thermo$c.csv";
  chmod 0777 ,"$dir/thermo/thermo$c.csv";
}
copy "$dir/thermo/reset.csv" ,"$dir/thermo/thermos.csv";
chmod 0777 ,"$dir/thermo/thermos.csv";

for(my $c=1;$c<=$locnum;$c++){
#  mkdir "$dir/rawdata/rawdata$c/today";
  copy "$dir/rawdata/reset.csv" ,"$dir/rawdata/rawdata$c.csv";
  chmod 0777 ,"$dir/rawdata/rawdata$c.csv";
}

for(my $c=1;$c<=$locnum;$c++){
  mkdir "$dir/photo/loc$c/today";
  chmod 0777 ,"$dir/photo/loc$c/today";
}

chmod 0777 ,"$dir/counter/acclog/acclog.csv";
chmod 0777 ,"$dir/hourfall/hourfall.csv";

#現在時刻取得
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year+=1900;
$mon+=1;
#２ケタ統一
if(length($mon) == 1){ $mon = "0$mon";}
if(length($mday) == 1){ $mday = "0$mday";}

    my $fileh = "$dir/hourfall/hourfall.csv";
    open (my $FH, ">>:encoding(cp932)", $fileh)
       or die qq/fall : Cant open file3 : $!/;
    print $FH "降積雪センサーネットワーク実証実験 日表$ln";
    print $FH "$year/$mon/$mday";
    print $FH ",東川口(川口支所),,,上川(旧泉水小学校),,,田麦山,,,木沢(やまぼうし),,,種苧原,,,西川口(保育園)$ln";
    for(my $c=1;$c<=5;$c++){
      print $FH ",積雪深[cm],時間降雪深[cm/h],平均気温[℃]";
    }
    print $FH "$ln";
    close $FH;

