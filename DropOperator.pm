#!/usr/bin/perl
package DropOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	my ($self, $exp) = @_;
	printf "DropOperator->apply(%s)\n", $exp;
	my $model = $self->{_model};
	my $value = $model->pop();
	if ($exp eq 'D') {
		print "Dropping all\n";
		while (defined($value)) {
			$value = $model->pop();
		}
	}
}

1;
