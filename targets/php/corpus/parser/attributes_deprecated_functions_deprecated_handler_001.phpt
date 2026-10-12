<?php

#[\Deprecated]
function my_exception_handler($e) {
	echo "Handled: ", $e->getMessage(), PHP_EOL;
};

set_exception_handler('my_exception_handler');

throw new \Exception('test');

?>