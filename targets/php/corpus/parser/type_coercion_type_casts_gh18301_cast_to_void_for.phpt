<?php

$count = 0;

#[NoDiscard]
function incCount() {
	global $count;
	$count++;
	return $count;
}

for ( $count = 0, (void)incCount(), incCount(); (void)incCount(), incCount() < 30; incCount(), $count++, incCount(), (void)incCount()) {
	echo $count . "\n";
}

?>