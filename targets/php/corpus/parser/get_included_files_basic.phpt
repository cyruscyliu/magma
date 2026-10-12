<?php

var_dump(get_included_files());

include(__DIR__."/get_included_files_basic.inc");
var_dump(get_included_files());

include_once(__DIR__."/get_included_files_basic.inc");
var_dump(get_included_files());

include(__DIR__."/get_included_files_basic.inc");
var_dump(get_included_files());

echo "Done\n";
?>