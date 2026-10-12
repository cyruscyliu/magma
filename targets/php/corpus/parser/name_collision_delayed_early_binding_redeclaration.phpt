<?php
class Foo {}
include __DIR__ . '/delayed_early_binding_redeclaration-1.inc';
include __DIR__ . '/delayed_early_binding_redeclaration-2.inc';
var_dump(class_exists(Bar::class));
?>