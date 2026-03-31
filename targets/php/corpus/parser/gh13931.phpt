<?php

register_shutdown_function(function() {
	var_dump(eval("return 1+3;"));
});

eval(<<<EVAL
function foo () {
    try {
        break;
    } finally {
    }
}
foo();
EVAL);

?>