import { Component } from '@angular/core';
import { LoginBannerComponent, LoginFooterComponent, LoginFormComponent } from '../../components';

@Component({
  selector: 'ig-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  standalone: true,
  imports: [LoginFormComponent, LoginBannerComponent, LoginFooterComponent]
})
export default class LoginComponent {

}
