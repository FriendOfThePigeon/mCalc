#!/usr/bin/perl
package PushOperator;
use strict;

use Object;

our @ISA = qw( Operator );

sub apply {
	my ($self, $value) = @_;
	$self->{_model}->push($value);
}

1;
