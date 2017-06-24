#! /usr/bin/perl

use XML::Simple;
use Data::Dumper;
{
    no warnings 'redefine';
    package Data::Dumper;
    sub qquote { return shift; }
}
$Data::Dumper::Useperl = 1;

require 'jcode.pl';
read( STDIN, $data, $ENV{ 'CONTENT_LENGTH' } );


my $ln = "\x0A";

#my $outputfn = "/var/www/snowmap/perl/senstemp.csv";
my $outthermofn = "/var/www/snowmap/log/thermo/thermo";
my $XML = "/var/www/snowmap/log/sens.xml";

my @time;
my $writeline;
my $locno;


# POSTデータの受け取り
$data =~ tr/+/ /;
$data =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;
&jcode'convert( *value, 'sjis' );
chomp $data;


print "Content-type: text/html\n\n";

print "---curl---$ln";

print "$data$ln";

$data =~ s/,/ /i;
($locno, $data) = split(/#/,$data);
print "locno = $locno$ln";
#$outputfn = $outputfn.".$locno";
$outthermofn = $outthermofn."$locno".".csv";

my $sensor;
($time, $sensor) = split(/-/,$data);
#if($locno==6){ $time=$time+11540405;}
print "$time, $sensor<br>$ln";

=pod
if($locno == 6){
	$temp = (1864.1 - 0.44*$sensor)/11.71;
}elsif($locno == 1){
	$temp = (1864.1 - 0.44*$sensor*2)/11.71 -1;
}elsif($locno == 5){
	$temp = (0.44*$sensor*2 - 600)/10;
}elsif($locno == 4){
	$temp = (0.44*$sensor - 600)/10;
}elsif($locno == 8){
	$temp = 0.44*$sensor;
}else{
	$temp = (1864.1 - 0.44*$sensor*2)/11.71;
}
$temp = sprintf("%.2f", $temp);
=cut

if($sensor>100){$sensor = $sensor-256;}
$temp = sprintf("%.2f", $sensor);

#print "temp = $temp$ln";

my $lines = "$time,$temp$ln";

&writefile($lines,$temp);

&changeXml();

sub writefile{

	my @wline = @_;

	print "wline is $ln $wline[0]";
	open(T, ">> $outthermofn") or die;
	flock(T, 2);
	print T $wline[0];
	close T;
	print qq{saved as <a href="$outthermofn">$outthermofn</a>};

}


sub changeXml{
	$locno--;

	my $ref = XMLin($XML);
	($time, my $msec) = split(/\./,$time);
	my @nowtime = split(/:| /,$time);

	my @pretime = split(/:| /,$ref->{loc}[$locno]->{thermotime});

	if($nowtime[1] > $pretime[1] || ($nowtime[1]==0 && $pretime[1]==23)){
		
		$ref->{loc}[$locno]->{thermotime0} = $time;
		$ref->{loc}[$locno]->{thermo0} = $temp;
		for(my $j=24; $j>=1; $j--){
			my $k = $j-1;
			my $thermo = "thermo$j";
			my $thermotime = "thermotime$j";
	#		if($j == 1){
	#			$ref->{loc}[$locno]->{$thermotime}
	#				 = $ref->{loc}[$locno]->{thermotime};
	#			$ref->{loc}[$locno]->{$thermo}
	#				 = $ref->{loc}[$locno]->{thermo};
	#		}else{
			my $prethermo = "thermo$k";
			my $prethermotime = "thermotime$k";
			$ref->{loc}[$locno]->{$thermotime}
				 = $ref->{loc}[$locno]->{$prethermotime};
			$ref->{loc}[$locno]->{$thermo}
				 = $ref->{loc}[$locno]->{$prethermo};
	#		}
		}
	}
	$ref->{loc}[$locno]->{thermotime} = $time;
	$ref->{loc}[$locno]->{thermo} = $temp;

#	print Dumper($ref);

	if(open(FH, "> $XML")){
		print "open $XML$ln";
		print FH XMLout($ref);
		print FH "\n";
		close(FH);
	}else{
		print "Error: Can't open $XML";
	}

	print "$ln---curl end---$ln";
}

