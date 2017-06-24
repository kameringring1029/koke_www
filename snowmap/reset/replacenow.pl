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


    my $fileh = "$dir/hourfall/hourfall.csv";
    open (my $FH, ">>:encoding(cp932)", $fileh)
       or die qq/fall : Cant open file3 : $!/;
    print $FH ",東川口(川口支所),,,上川(旧泉水小学校),,,木沢(やまぼうし),,,中山(サンローラ),,,田麦山$ln";
    for(my $c=1;$c<=5;$c++){
      print $FH ",積雪深[cm],降雪深[[cm],平均気温[℃]";
    }
    print $FH "$ln";
    close $FH;

