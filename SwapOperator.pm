#!/usr/bin/perl
package SwapOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	my ($self, $value) = @_;
	my $model = $self->{_model};
	my ($value1, $value2) = map { $model->pop() } (1, 2);
	if (!defined($value1)) {
		return;
	}
	if (!defined($value2)) {
		$model->push($value1);
		return;
	}
	$model->push($value1);
	$model->push($value2);
}

1;
