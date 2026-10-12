<?php

interface A {}
interface B {}

function test(): (A&B)|A {}

?>
===DONE===