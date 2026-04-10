<?php

class C {
    function handle() {}
    static function handleStatic() {}
}

class Invokable {
    public function __invoke() {
    }
}

function foo() {}

echo "No exception handler\n";
var_dump(get_exception_handler() === null);

echo "\nFunction string\n";
set_exception_handler('foo');
var_dump(get_exception_handler() === 'foo');

echo "\nNULL\n";
set_exception_handler(null);
var_dump(get_exception_handler() === null);

echo "\nStatic method array\n";
set_exception_handler([C::class, 'handleStatic']);
var_dump(get_exception_handler() === [C::class, 'handleStatic']);

echo "\nStatic method string\n";
set_exception_handler('C::handleStatic');
var_dump(get_exception_handler() === 'C::handleStatic');

echo "\nInstance method array\n";
set_exception_handler([$c = new C(), 'handle']);
var_dump(get_exception_handler() === [$c, 'handle']);

echo "\nFirst class callable method\n";
set_exception_handler($f = (new C())->handle(...));
var_dump(get_exception_handler() === $f);

echo "\nClosure\n";
set_exception_handler($f = function () {});
var_dump(get_exception_handler() === $f);

echo "\nInvokable\n";
set_exception_handler($object = new Invokable());
var_dump(get_exception_handler() === $object);

echo "\nStable return value\n";
var_dump(get_exception_handler() === get_exception_handler());

?>==DONE==