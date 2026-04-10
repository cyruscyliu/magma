<?php

#[AllowDynamicProperties]
class ByRef {
    public $plain = 'plain';
    private $_virtualByRef = 'virtualByRef';
    public $virtualByRef {
        &get {
          echo __METHOD__, "\n";
          return $this->_virtualByRef;
        }
        set {
          echo __METHOD__, "\n";
          $this->_virtualByRef = $value;
        }
    }
    public $virtualSetOnly {
        set {
            echo __METHOD__, "\n";
        }
    }
    public function __construct() {
        $this->undef = 'dynamic';
        $this->dynamic = 'dynamic';
        unset($this->undef);
    }
}

#[AllowDynamicProperties]
class ByVal extends ByRef {
    private $_virtualByVal = 'virtualByVal';
    public $virtualByVal {
        get {
          echo __METHOD__, "\n";
          return $this->_virtualByVal;
        }
        set {
          echo __METHOD__, "\n";
          $this->_virtualByVal = $value;
        }
    }
    public $backed = 'backed' {
        get {
          echo __METHOD__, "\n";
          return $this->backed;
        }
        set {
          echo __METHOD__, "\n";
          $this->backed = $value;
        }
    }
    public string $backedUninitialized {
        get {
          echo __METHOD__, "\n";
          $this->backedUninitialized ??= 'backedUninitialized';
          return $this->backedUninitialized;
        }
        set {
          echo __METHOD__, "\n";
          $this->backedUninitialized = $value;
        }
    }
}

function testByRef($object) {
    foreach ($object as $prop => &$value) {
        echo "$prop => $value\n";
        $value = strtoupper($value);
    }
    unset($value);
    var_dump($object);
}

function testByVal($object) {
    foreach ($object as $prop => $value) {
        echo "$prop => $value\n";
        $object->{$prop} = strtoupper($value);
    }
    var_dump($object);
}

testByVal(new ByVal);
testByVal(new ByRef);
testByRef(new ByRef);

class A {
    private $changed { get => 'A'; }
    protected $promoted { get => 'A'; }
    protected $protected { get => 'A'; }
    private $shadowed = 'A';

    public function test() {
        foreach ($this as $k => $v) {
            var_dump($k, $v);
        }
    }
}

#[AllowDynamicProperties]
class B extends A {
    public $changed { get => 'B'; }
    public $promoted { get => 'B'; }
}

$b = new B;
$b->shadowed = 'Global';
$b->test();

?>