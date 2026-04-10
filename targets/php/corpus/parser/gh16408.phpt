<?php
$counter = 0;
ob_start(function ($buffer) use (&$c, &$counter) {
        $c = 0;
        ++$counter;
        return '';
}, 1);
$c .= [];
$c .= [];
ob_end_clean();
echo $counter . "\n";
?>