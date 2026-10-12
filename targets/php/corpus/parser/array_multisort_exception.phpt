<?php
$array = [1 => new DateTime(), 0 => new DateTime()];
array_multisort($array, SORT_STRING);
?>