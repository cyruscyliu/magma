<?php
class ParentC {}
class Child extends ParentC {
    public $a {
        get {
            return parent::${0}::get ();
        }
    }
}
?>