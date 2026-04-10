<?php

set_error_handler(function($errno, $msg) {
    throw new Exception($msg);
});

class C implements Serializable {
    public function serialize() {}
    public function unserialize($serialized) {}
}

?>