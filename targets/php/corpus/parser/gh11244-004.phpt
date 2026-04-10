<?php

$obj = (object)[1,2,3];

foreach ($obj as $p => $v) {
    echo "$p : $v\n";
    $clone = clone $obj;
    $ref = &$obj->$p;
}

?>