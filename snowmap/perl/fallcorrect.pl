#! /usr/bin/perl

=pod
use warnings;
use strict;
=cut

use Encode;
use utf8;

use XML::Simple;
use Data::Dumper;
{
    no warnings 'redefine';
    package Data::Dumper;
    sub qquote { return shift; }
}
$Data::Dumper::Useperl = 1;


my $ln = "\x0A";

my $locnum = 6;

my $outputfn = "/var/www/snowmap/log/hourfall/hourfall.csv";
my $outputdir = "/var/www/snowmap/log/hourfall/";
my $XML = "/var/www/snowmap/log/sens.xml.read";

my @sc; my @fall; my @thermo; my $time; my $wline;


system "cp /var/www/snowmap/log/sens.xml /var/www/snowmap/log/sens.xml.read";

&readXml();


# XML読み込み
sub readXml{

	print "$ln---readXml---$ln";

	($sec, $min, $hour, $mday, $mon, $year) = localtime;
	$year += 1900; $mon += 1;


	if($hour != 0){	
		$hour--;
		if($hour == 8){
			my $mday9 = $mday-1;
			if(length($mon) == 1){ $mon = "0$mon";}
			if(length($mday) == 1){ $mday9 = "0$mday9";}
			$outputfn = $outputdir."$year-$mon-$mday9.csv";
		}
	}else{
		$hour = 23; $mday--;
		#２ケタ統一
		if(length($mon) == 1){ $mon = "0$mon";}
		if(length($mday) == 1){ $mday = "0$mday";}

	}


	$wline = "$hour:00";
#	$wline = "$year/$mon/$mday $hour:00";
#	$wline = $wline."時台";


	$ref = XMLin($XML);

	for(my $i=0; $i<=($locnum-1); $i++){
		$sc[$i] = $ref->{loc}[$i]->{sc1};
		$fall[$i] = $ref->{loc}[$i]->{fall1};
		$thermo[$i] = $ref->{loc}[$i]->{thermo1};
#		if($i==3){
#			$wline = $wline.",$sc[$i],$fall[$i]";
#		}elsif($i==2){
#			my $thermo4 = $thermo[$i]*0.8+0.4;
#			$wline = $wline.",$thermo4";
#			$wline = $wline.",$sc[$i],$fall[$i],$thermo[$i]";
#		}else{
			$wline = $wline.",$sc[$i],$fall[$i],$thermo[$i]";
#		}
	}

	$wline = $wline."$ln";

	&writeFile();

}


# データ書込み
sub writeFile{

	# CSV出力
	if(open(F, ">>:encoding(cp932)" ,$outputfn)){
		flock(F, 2);
		print F "$wline";
		close F;
	}else{
		print "error: Can't open $outputfn$ln";
	}

	print qq{saved as <a href="$outputfn">$outputfn</a>};

	print "$ln---End correct---$ln";
}


