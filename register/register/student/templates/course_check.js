<script type="text/javascript">
    var NewCount = 0
    alert("Hello")
    function checkCourseCount() {
        if (document.getElementById("elective").checked)
            {NewCount = NewCount + 1}

        if (NewCount == 1)
        {
            alert('You cannot select more electives.')
            document.elective; return false;
        }
    }
</script>