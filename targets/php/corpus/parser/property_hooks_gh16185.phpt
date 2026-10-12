<?php

class ByRef {
    private $_virtualByRef = 'virtualByRef';
}

class ByVal extends ByRef {
    public $_virtualByRef {
        get => null;
        set { $this->dynamicProp = $value; }
    }
}

$object = new ByVal;
foreach ($object as $value) {
    var_dump($value);
    $object->_virtualByRef = $value;
}

?>