#! /usr/bin/perl

=pod
use warnings;
use strict;
=cut

use Encode;
use utf8;
binmode STDIN,  ":encoding(cp932)";
binmode STDOUT, ":encoding(cp932)";

use XML::Simple;
use Data::Dumper;
{
    no warnings 'redefine';
    package Data::Dumper;
    sub qquote { return shift; }
}
$Data::Dumper::Useperl = 1;


my $ln = "\x0A";

## 予測に用いるセンサデータのセンサノードID ##
my $locno = 2;
my $scat=0; my $fall=0; my $scattime=0;

my $XML = "/var/www/snowmap/log/sens.xml";
my $inputfn = "/var/www/snowmap/perl/scat.csv";
$inputfn = $inputfn.".$locno";


## 現時刻取得 ##
my ($nowsec, $nowmin, $nowhour, $nowmday, $nowmon, $nowyear) = localtime(time);
$nowyear += 1900; $nowmon += 1;
print "now :: $nowmday $nowhour:$nowmin$ln";


&estimation();


sub estimation{
	#読み込みファイル
	open my $FR, "<$inputfn"
	  or die qq/ Cant open file : $!/;

	#ファイル読み込み
	while(my $line = <$FR>){
		$line =~ s/\r+\n//g;
		chomp($line);
		my @lines = split(/,/, $line);
		
		my ($sec, $min, $hour, $mday, $mon, $year) = localtime($lines[0]);
		$year += 1900; $mon += 1;

		if(($hour>=17 && $mday==($nowmday-1))||($hour<2 && $mday==$nowmday)){
			if($lines[1]>=0.1){$scattime = $scattime + 10;}
			$fall = $fall + $lines[2];
			print "$hour:$min $fall/$scattime$ln";
		}	 
  	}

	## read temparture ##
	my $ref = XMLin($XML);
	my $temp = $ref->{loc}[$locno-1]->{thermo};

	## calculate future snowfall ##
	$scattime = $scattime/60;
	my $estimate_fall = $fall/$scattime * 5.41;
	$estimate_fall = sprintf("%.0f", $estimate_fall);
	print "est=$estimate_fall; scattime=$scattime, fall=$fall, temp=$temp$ln";


	## send mail ##
	## configuration ##
	my $destination = "\@docomo.ne.jp";
	my $BCC = "\@stn.nagaokaut.ac.jp";
	my $subject = "$nowmon/$nowmday:降雪予測メール";

	## mail main ##
	my $text = "\n
	 17時から2時までの降雪：$fall\[cm]
	 現在の気温：$temp\[℃]
	 2時から7時までの予測降雪：$estimate_fall\[cm]\n
	 ※積雪の上で測定しているため，道路上より多く見積もられます
	";

	## send ##
	my $name = &getname();
	my $result = qx/echo "$text$name" | nkf -s | mail -s `echo "$subject" | nkf -s` $destination/;
	$result = qx/echo "$text$name" | nkf -s | mail -s `echo "$subject" | nkf -s` $BCC/;
}


# 署名
sub getname{

my $name="
\n
--------
署名事項：
降積雪センサネットワークシステム
--------
\n";

return $name;

}

