<?php
$x = 'non-empty';
ob_start(function () use (&$c) {
	$c = 0;
	return '';
}, 1);
$c = [];
$x = $c . $x;
$x = $c . $x;
ob_end_clean();
echo "Done\n";
?>