#!/usr/bin/perl
package ClearHistoryOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	my ($self, $exp) = @_;
	printf "ClearHistoryOperator->apply(%s)\n", $exp;
	my $model = $self->{_model};
	$model->clear_history();
}

1;
