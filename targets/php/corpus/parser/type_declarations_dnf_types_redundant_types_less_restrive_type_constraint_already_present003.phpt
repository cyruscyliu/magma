<?php

interface A {}
interface B {}
interface C {}

function test(): (A&B)|(A&B&C) {}

?>
===DONE===