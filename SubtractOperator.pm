#!/usr/bin/perl
package SubtractOperator;
use strict;

use BinaryOperator;

our @ISA = qw( BinaryOperator );

sub binary_apply {
	my ($self, $value1, $value2) = @_;
	return ($value2 - $value1);
}

1;
