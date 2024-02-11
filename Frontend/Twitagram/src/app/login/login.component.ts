import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  user = {
    username: '',
    password: '',
  };

  currentUser: any;

  constructor(private apiService: ApiService, private router: Router, private toastr: ToastrService) {

  }

  onLogin() {
    this.apiService.login(this.user).subscribe(
      (data: any) => {
        console.log(data);
        localStorage.setItem('token', data.access);
        localStorage.setItem('username', data.username);

        this.apiService.getUserProfile(data.username).subscribe((data: any) => {
          console.log("User id : " + JSON.stringify(data.id));
          localStorage.setItem('currentUserId', JSON.stringify(data.id));

        })

        this.toastr.success('Login Successful - Redirecting to feed!');
        this.router.navigate(['/posts/feed']);
        
      },
      (error: any) => {
        console.error(error);
        this.toastr.error('Login Failed !');
        this.user.username = '';
        this.user.password = '';
      });


  };

}
