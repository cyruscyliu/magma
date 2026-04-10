<?php

$a = "test\0test";
$$a;
$a = "\0test";
$$a;
$a = "test\0";
$$a;

$GLOBALS["test\0test"];
$GLOBALS["\0test"];
$GLOBALS["test\0"];

compact("a\0b");
compact("\0ab");
compact("ab\0");

?>