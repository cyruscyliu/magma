<?php
class Thing {}
function boom()
{
    $reader = xml_parser_create();
    $thing = new Thing();
    xml_set_object($reader, $thing);
    die("ok\n");
}
boom();
?>