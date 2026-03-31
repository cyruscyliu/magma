<?php

$anonymous = new class(){};

throw new Exception(
    get_class($anonymous).' ...now you don\'t!',
    E_USER_ERROR
);

?>