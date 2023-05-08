package com.example.plant_identification;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.widget.ImageButton;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {
    private ImageButton button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Create onClickListener to allow button to open new activity (9/8/22)
        //Changed Button to ImageButton to display UI correctly (11/13/22)
        button = (ImageButton) findViewById(R.id.Launch);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openCamera();
            }
        });
    }

    public void openCamera() {
        Intent intent = new Intent(this, camera.class);
        startActivity(intent);
    }
}