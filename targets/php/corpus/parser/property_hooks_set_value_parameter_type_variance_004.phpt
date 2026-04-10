<?php

spl_autoload_register(function ($className) {
    echo "Autoloading $className\n";
});

include __DIR__ . "/set_value_parameter_type_variance_004.inc";

?>