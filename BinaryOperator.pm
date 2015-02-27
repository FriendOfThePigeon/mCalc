#!/usr/bin/perl
package BinaryOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub get_symbol {
	return '?';
}

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
	my $result = $self->binary_apply($value1, $value2);
	my $description = sprintf('%s %s %s', $value2, $self->get_symbol(), $value1);
	$model->push_result($result, $description);
}

1;
