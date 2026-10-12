<?php
echo "Test case to ensure the issue is fixed.\n";
var_dump(stripos('aaBBBBBb', 'b'));
var_dump(stripos('aaBBBBBbb', 'b'));
var_dump(stripos('aaBBBBBbbb', 'b'));
var_dump(stristr('aaBBBBBb', 'b'));
var_dump(stristr('aaBBBBBbb', 'b'));
var_dump(stristr('aaBBBBBbbb', 'b'));

echo "\n";
echo "Test cases to ensure the original functionality is not broken.\n";
var_dump(stripos('aaBBBBBbc', 'c'));
var_dump(stripos('aaBBBBBbC', 'c'));
var_dump(stristr('aaBBBBBbc', 'c'));
var_dump(stristr('aaBBBBBbC', 'c'));
?>