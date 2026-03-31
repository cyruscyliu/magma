<?php
ini_set("fiber.stack_size","-1");
$fiber = new Fiber(function() {});
try {
    $fiber->start();
} catch (Throwable $e) {
	echo "Exception: " . $e->getMessage()."\n";
}
?>
DONE