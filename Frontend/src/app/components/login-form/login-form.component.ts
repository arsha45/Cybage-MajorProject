import { Component } from '@angular/core';
import {CardModule} from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { Divider, DividerModule } from 'primeng/divider';

@Component({
  selector: 'ig-login-form',
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.css',
  standalone:true,
  imports: [
    CardModule,
    InputTextModule,
    ButtonModule,
    DividerModule
  ]
})
export default class LoginFormComponent {

}
