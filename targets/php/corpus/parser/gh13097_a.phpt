<?php

$anonymous = new class(){};

trigger_error(
    get_class($anonymous).' ...now you don\'t!',
    E_USER_ERROR
);

?>