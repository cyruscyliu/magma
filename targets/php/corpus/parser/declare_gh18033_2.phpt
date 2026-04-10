<?php
ob_start(function() {
    declare(ticks=1);
    register_tick_function(
       function() { }
    );
    return '';
});
?>