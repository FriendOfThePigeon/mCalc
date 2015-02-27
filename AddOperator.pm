#!/usr/bin/perl
package AddOperator;
use strict;

use BinaryOperator;

our @ISA = qw( BinaryOperator );

sub get_symbol {
	return '+';
}

sub binary_apply {
	my ($self, $value1, $value2) = @_;
	return ($value1 + $value2);
}

1;
