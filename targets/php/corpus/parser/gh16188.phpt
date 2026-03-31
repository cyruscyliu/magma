<?php

$re = new TypeError();
array_walk($re, function (&$item, $key) use (&$re) {
    if ($key === "\x00Error\x00previous") {
        $item = new Exception();
    }
});
printf("getTraceAsString:\n%s\n\n", $re->getTraceAsString());
printf("getPrevious:\n%s\n\n", get_class($re->getPrevious()));
printf("__toString:\n%s\n\n", $re);

?>
==DONE==