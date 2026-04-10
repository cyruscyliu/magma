<?php
namespace Foo;
function declare_local_class_exists() {
    function class_exists() {
        var_dump(__FUNCTION__);
        return true;
    }
}
declare_local_class_exists();
var_dump(CLASS_EXISTS('Foo'));
?>