<?php

$floats = array(
    076545676543223,
    032325463734,
    0777777,
    07777777777777,
    033333333333333,
    );

foreach ($floats as $d) {
    $l = (float)$d;
    var_dump($l);
}

echo "Done\n";
?>