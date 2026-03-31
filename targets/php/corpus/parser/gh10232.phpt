<?php

set_include_path('gh10232-nonexistent') or exit(1);
chdir(__DIR__) or exit(1);

spl_autoload_register(function () {
    trigger_error(__LINE__);
    $ex = new Exception();
    echo 'Exception on line ', $ex->getLine(), "\n";
    require_once __DIR__ . '/gh10232/constant_def.inc';
}, true);


class ConstantRef
{
    public const VALUE = ConstantDef::VALUE;
}

ConstantRef::VALUE;

?>